#!/usr/bin/env python

# Author: Shao Zhang and Phil Saltzman
# Models: Eddie Canaan
# Last Updated: 2015-03-13
#
# This tutorial shows how to determine what objects the mouse is pointing to
# We do this using a collision ray that extends from the mouse position
# and points straight into the scene, and see what it collides with. We pick
# the object with the closest collision


# -----------------------------------
# This section of code is for installing specific libraries not included in python
# If libraries are already installed, comment out runInstall()

import os

#from direct.showbase.ShowBaseGlobal import render2d


def runInstall():
    print("Installing needed libraries")
    os.system("pip install panda3d")
    os.system("pip install pygame")
    os.system("pip install moviepy")

#runInstall()

# -----------------------------------


from direct.showbase.ShowBase import ShowBase
from panda3d.core import CollisionTraverser, CollisionNode, CardMaker
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LPoint3, LVector3, BitMask32
from direct.gui.DirectGui import *
from direct.task.Task import Task

from moviepy.editor import *
import pygame

import sys
#from direct.showbase.DirectObject import DirectObject
#from panda3d.core import LightAttrib

# Colors
SQUAREBLACK = (0, 0, 0, 1)
SQUAREWHITE = (1, 1, 1, 1)
HIGHLIGHT1 = (0, 1, 1, 1)
HIGHLIGHT2 = (1, 1, 0, 1)
PIECEBLACK = (.15, .15, .15, 1)
PIECEWHITE = (1, 1, 1, 1)


# Now we define some helper functions that we will need later

# This function, given a line (vector plus origin point) and a desired z value,
# will give us the point on the line where the desired z value is what we want.
# This is how we know where to position an object in 3D space based on a 2D mouse
# position. It also assumes that we are dragging in the XY plane.
#
# This is derived from the mathematical of a plane, solved for a given point
def PointAtZ(z, point, vec):
    return point + vec * ((z - point.getZ()) / vec.getZ())

# A handy little function for getting the proper position for a given square1
def SquarePos(i):
    return LPoint3((i % 8) - 3.5, int(i // 8) - 3.5, 0)

# Helper function for determining whether a square should be white or black
# The modulo operations (%) generate the every-other pattern of a chess-board
def SquareColor(i):
    if (i + ((i // 8) % 2)) % 2:
        return SQUAREBLACK
    else:
        return SQUAREWHITE

class ChessboardDemo(ShowBase):
    def __init__(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
        ShowBase.__init__(self)

        self.WhiteTurn = True

        # This code puts the standard title and instruction text on screen
        self.title = OnscreenText(
            text="Chess 2",
            style=1, fg=(1, 1, 1, 1), shadow=(0, 0, 0, 1),
            pos=(0.8, -0.95), scale = .07)
        self.escapeEvent = OnscreenText(
            text="ESC: Quit", parent=base.a2dTopLeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.1),
            align=TextNode.ALeft, scale = .05)
        self.mouse1Event = OnscreenText(
            text="Left-click and drag: Pick up and drag piece",
            parent=base.a2dTopLeft, align=TextNode.ALeft,
            style=1, fg=(1, 1, 1, 1), pos=(0.06, -0.16), scale=.05)

        self.accept('escape', sys.exit)  # Escape quits
        self.disableMouse()  # Disable mouse camera control
        camera.setPosHpr(0, -12, 8, 0, -35, 0)  # Set the camera
        self.setupLights()  # Setup default lighting

        # Since we are using collision detection to do picking, we set it up like
        # any other collision detection system with a traverser and a handler
        self.picker = CollisionTraverser()  # Make a traverser
        self.pq = CollisionHandlerQueue()  # Make a handler
        # Make a collision node for our picker ray
        self.pickerNode = CollisionNode('mouseRay')
        # Attach that node to the camera since the ray will need to be positioned
        # relative to it
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        # Everything to be picked will use bit 1. This way if we were doing other
        # collision we could separate it
        self.pickerNode.setFromCollideMask(BitMask32.bit(1))
        self.pickerRay = CollisionRay()  # Make our ray
        # Add it to the collision node
        self.pickerNode.addSolid(self.pickerRay)
        # Register the ray as something that can cause collisions
        self.picker.addCollider(self.pickerNP, self.pq)
        # self.picker.showCollisions(render)

        # Now we create the chess board and its pieces

        # We will attach all of the squares to their own root. This way we can do the
        # collision pass just on the squares and save the time of checking the rest
        # of the scene
        self.squareRoot = render.attachNewNode("squareRoot")

        # For each square
        self.squares = [None for i in range(64)]
        self.pieces = [None for i in range(64)]
        for i in range(64):
            # Load, parent, color, and position the model (a single square
            # polygon)
            self.squares[i] = loader.loadModel("models/square")
            self.squares[i].reparentTo(self.squareRoot)
            self.squares[i].setPos(SquarePos(i))
            self.squares[i].setColor(SquareColor(i))
            # Set the model itself to be collideable with the ray. If this model was
            # any more complex than a single polygon, you should set up a collision
            # sphere around it instead. But for single polygons this works
            # fine.
            self.squares[i].find("**/polygon").node().setIntoCollideMask(
                BitMask32.bit(1))
            # Set a tag on the square's node so we can look up what square this is
            # later during the collision pass
            self.squares[i].find("**/polygon").node().setTag('square', str(i))

            # We will use this variable as a pointer to whatever piece is currently
            # in this square

        # The order of pieces on a chessboard from white's perspective. This list
        # contains the constructor functions for the piece classes defined
        # below
        pieceOrder = (Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook)

        for i in range(8, 16):
            # Load the white pawns
            self.pieces[i] = Pawn(i, PIECEWHITE, "W")
        for i in range(48, 56):
            # load the black pawns
            self.pieces[i] = Pawn(i, PIECEBLACK, "B")
        for i in range(8):
            # Load the special pieces for the front row and color them white
            self.pieces[i] = pieceOrder[i](i, PIECEWHITE, "W")
            # Load the special pieces for the back row and color them black
            self.pieces[i + 56] = pieceOrder[i](i + 56, PIECEBLACK, "B")

        # This will represent the index of the currently highlited square
        self.hiSq = False
        # This wil represent the index of the square where currently dragged piece
        # was grabbed from
        self.dragging = False

        # Start the task that handles the picking
        self.mouseTask = taskMgr.add(self.mouseTask, 'mouseTask')
        self.accept("mouse1", self.grabPiece)  # left-click grabs a piece
        self.accept("mouse1-up", self.releasePiece)  # releasing places it

        #self.setupMenu()

    # TODO create basic startup menu
    def setupMenu(self):

        # Add some text
        bk_text = "This is my Demo"
        menuImage = OnscreenImage(image="images/Chess_Menu_Image.png")

        textObject = OnscreenText(text=bk_text, pos=(0.95, -0.95), scale=0.07,
                                  fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                                  mayChange=1)

        # Callback function to set  text
        def setText():
            b.destroy()
            menuImage.destroy()
            textObject.destroy()

        # Add button
        b = DirectButton(text=("OK", "click!", "rolling over", "disabled"),
                         scale=.05, command=setText)

    # This function swaps the positions of two pieces
    def swapPieces(self, fr, to):
        temp = self.pieces[fr]
        self.pieces[fr] = self.pieces[to]
        self.pieces[to] = temp
        if self.pieces[fr]:
            self.pieces[fr].square = fr
            self.pieces[fr].obj.setPos(SquarePos(fr))
        if self.pieces[to]:
            self.pieces[to].square = to
            self.pieces[to].obj.setPos(SquarePos(to))

    # This function captures a piece
    def capturePieces(self, fr, to):
        KillerColor = self.pieces[fr].PieceColor
        KillerName = self.pieces[fr].PieceName
        KilledName = self.pieces[to].PieceName

        self.pieces[to].obj.hide()
        self.pieces[to] = self.pieces[fr]
        self.pieces[fr] = None
        if self.pieces[to]:
            self.pieces[to].square = to
            self.pieces[to].obj.setPos(SquarePos(to))

        CaptureVideo = KillerColor + KillerName + "K" + KilledName
        if CaptureVideo in videos:
            videos[CaptureVideo].preview()
            pygame.quit()
        else:
            print("Video not yet made")

    def mouseTask(self, task):
        # This task deals with the highlighting and dragging based on the mouse

        # First, clear the current highlight
        if self.hiSq is not False:
            self.squares[self.hiSq].setColor(SquareColor(self.hiSq))
            self.hiSq = False

        # Check to see if we can access the mouse. We need it to do anything
        # else
        if self.mouseWatcherNode.hasMouse():
            # get the mouse position
            mpos = self.mouseWatcherNode.getMouse()

            # Set the position of the ray based on the mouse position
            self.pickerRay.setFromLens(self.camNode, mpos.getX(), mpos.getY())

            # If we are dragging something, set the position of the object
            # to be at the appropriate point over the plane of the board
            if self.dragging is not False:
                # Gets the point described by pickerRay.getOrigin(), which is relative to
                # camera, relative instead to render
                nearPoint = render.getRelativePoint(
                    camera, self.pickerRay.getOrigin())
                # Same thing with the direction of the ray
                nearVec = render.getRelativeVector(
                    camera, self.pickerRay.getDirection())
                self.pieces[self.dragging].obj.setPos(
                    PointAtZ(.5, nearPoint, nearVec))

            # Do the actual collision pass (Do it only on the squares for
            # efficiency purposes)
            self.picker.traverse(self.squareRoot)
            if self.pq.getNumEntries() > 0:
                # if we have hit something, sort the hits so that the closest
                # is first, and highlight that node
                self.pq.sortEntries()
                i = int(self.pq.getEntry(0).getIntoNode().getTag('square'))
                # Set the highlight on the picked square
                if self.WhiteTurn:
                    self.squares[i].setColor(HIGHLIGHT1)
                else:
                    self.squares[i].setColor(HIGHLIGHT2)
                self.hiSq = i

        return Task.cont

    def grabPiece(self):
        # If a square is highlighted and it has a piece, set it to dragging
        # mode
        if self.hiSq is not False and self.pieces[self.hiSq]:
            self.dragging = self.hiSq
            self.hiSq = False

    def releasePiece(self):
        # Letting go of a piece. If we are not on a square, return it to its original
        # position. Otherwise, swap it with the piece in the new square
        # Make sure we really are dragging something
        if self.dragging is not False:
            # Check if the piece we are moving is allowed to move
            CorrectColor = False
            if self.WhiteTurn and self.pieces[self.dragging].PieceColor == "W":
                CorrectColor = True
            elif not self.WhiteTurn and self.pieces[self.dragging].PieceColor == "B":
                CorrectColor = True

            # Either we have let go of the piece but we are not on a square,
            # or we have tried to move a piece when it is not their turn
            if self.hiSq is False or CorrectColor is False:
                # Piece is moved out of bounds, return it to old square
                self.pieces[self.dragging].obj.setPos(
                    SquarePos(self.dragging))

            else:
                # Piece has moved to a valid square
                # Check if we have moved to a square with a piece on it already
                if self.pieces[self.hiSq] is None:
                    self.swapPieces(self.dragging, self.hiSq)
                    self.WhiteTurn = not self.WhiteTurn
                else:
                    # TODO check if a valid move mas been made
                    if self.pieces[self.dragging].PieceColor is not self.pieces[self.hiSq].PieceColor:
                        self.capturePieces(self.dragging, self.hiSq)
                        self.WhiteTurn = not self.WhiteTurn
                    else:
                        self.pieces[self.dragging].obj.setPos(
                            SquarePos(self.dragging))

        # We are no longer dragging anything
        self.dragging = False

    # This function sets up some default lighting
    def setupLights(self):
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((.8, .8, .8, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 45, -45))
        directionalLight.setColor((0.2, 0.2, 0.2, 1))
        render.setLight(render.attachNewNode(directionalLight))
        render.setLight(render.attachNewNode(ambientLight))

# Superclass for a piece
class Piece(object):
    PieceName = ""
    PieceColor = ""

    def __init__(self, square, color, ColorName):
        self.obj = loader.loadModel(self.model)
        self.obj.reparentTo(render)
        self.obj.setColor(color)
        self.obj.setPos(SquarePos(square))
        self.PieceColor = ColorName

# Classes for each type of chess piece

#TODO replace models with current BLender models
class Pawn(Piece):
    model = "models/pawn"
    PieceName = "Pawn"

class King(Piece):
    model = "models/king"
    PieceName = "King"

class Queen(Piece):
    model = "models/queen"
    PieceName = "Queen"

class Bishop(Piece):
    model = "models/bishop"
    PieceName = "Bishop"

class Knight(Piece):
    model = "models/knight"
    PieceName = "Knight"

class Rook(Piece):
    model = "models/rook"
    PieceName = "Rook"

videos = {}
def setupVideos():
    AllNames = {0: "Pawn", 1: "King", 2: "Queen", 3: "Bishop", 4: "Knight", 5: "Rook"}
    print("Loading capture animations")
    for i in range(0, 6):
        for ii in range(0, 6):
            BVideoFile = "captures/" + "B" + AllNames[i] + "K" + AllNames[ii] + ".mkv"
            WVideoFile = "captures/" + "W" + AllNames[i] + "K" + AllNames[ii] + ".mkv"
            # If the file exists then add it to the videos dictionary
            if os.path.isfile(BVideoFile):
                videosIndex = "B" + AllNames[i] + "K" + AllNames[ii]
                videos[videosIndex] = VideoFileClip(BVideoFile)
                videos[videosIndex].set_fps(24)
            else:
                print(BVideoFile + " not found")
            if os.path.isfile(WVideoFile):
                videosIndex = "W" + AllNames[i] + "K" + AllNames[ii]
                videos[videosIndex] = VideoFileClip(WVideoFile)
                videos[videosIndex].set_fps(24)
            else:
                print(WVideoFile + " not found")
    print("Captures loaded")

def runGame():
    demo = ChessboardDemo()
    # Run demo step once to load window then load needed game resources
    demo.taskMgr.step()
    setupVideos()
    # Continue running game
    demo.run()

runGame()