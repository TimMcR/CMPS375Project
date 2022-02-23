# TODO create basic startup menu
# TODO check if a valid move mas been made
# TODO replace models with current Blender models
# TODO make basic moving animations for each piece

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
from direct.actor.Actor import Actor
from direct.interval.MetaInterval import Sequence
from direct.interval.IntervalGlobal import *


#from . import Interval

from moviepy.editor import *
import pygame

import sys
#from direct.showbase.DirectObject import DirectObject
#from panda3d.core import LightAttrib

def convertRGB(red, green, blue):
    return (red/255, green/255, blue/255, 1)

# Colors
SQUAREBLACK = convertRGB(139, 69, 16)
SQUAREWHITE = convertRGB(255, 248, 220)
HIGHLIGHT1 = convertRGB(0, 255, 255)
HIGHLIGHT2 = convertRGB(255, 0, 255)
PIECEBLACK = convertRGB(0, 0, 0)
PIECEWHITE = convertRGB(255, 255, 255)

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

def CenterPos(Start, End, z):
    startX = Start.getX()
    startY = Start.getY()
    endX = End.getX()
    endY = End.getY()
    newX = (startX + endX) / 2
    newY = (startY + endY) / 2
    return LPoint3(newX, newY, z)

class ChessGame(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.videos = {}

    def step(self):
        self.taskMgr.step()

    # Run just to set up menu without start button
    def setupMenuWait(self):
        self.menuImage = OnscreenImage(image="images/Chess_Menu_Image.png", scale=1.4)

        self.menuText = OnscreenText(text="CHESS 2", pos=(0.95, -0.95), scale=0.07,
                                     fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                                     mayChange=1)

        self.menuButton = DirectButton(text="START",
                                       scale=.05, command=self.closeMenu)
        self.menuButton.hide()

        # Step twice to properly load start menu
        self.step()
        self.step()

    def setupMenuReady(self):
        self.setupMenuWait()
        self.showMenuButton()

    def closeMenu(self):
        self.menuButton.destroy()
        self.menuImage.destroy()
        self.menuText.destroy()
        self.setupGame()

    def showMenuButton(self):
        self.menuButton.show()

    def setupGame(self):
        # Initialize the ShowBase class from which we inherit, which will
        # create a window and set up everything we need for rendering into it.
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
        if CaptureVideo in self.videos:
            self.videos[CaptureVideo].preview()
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
            IsWhite = self.pieces[self.dragging].PieceColor == "W"
            if self.WhiteTurn and IsWhite:
                CorrectColor = True
            elif not self.WhiteTurn and not IsWhite:
                CorrectColor = True

            # Either we have let go of the piece but we are not on a square,
            # or we have tried to move a piece when it is not their turn
            if self.hiSq is False or CorrectColor is False:
                # Return piece to previous square
                self.pieces[self.dragging].obj.setPos(
                    SquarePos(self.dragging))

            else:
                # Piece has moved to a valid square
                # Check if we have moved to a square with a piece on it already
                DragPiece = self.pieces[self.dragging]
                HitPiece = self.pieces[self.hiSq]
                if HitPiece is None:
                    startPosition = SquarePos(self.dragging)
                    endPosition = SquarePos(self.hiSq)
                    if(DragPiece.HasAnimation):
                        DragPiece.runAnimation(startPosition, endPosition)

                    self.swapPieces(self.dragging, self.hiSq)
                    self.WhiteTurn = not self.WhiteTurn
                else:
                    if DragPiece.PieceColor is not HitPiece.PieceColor:
                        self.capturePieces(self.dragging, self.hiSq)
                        self.WhiteTurn = not self.WhiteTurn
                    else:
                        DragPiece.obj.setPos(
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

    def setupVideos(self):
        AllNames = {0: "Pawn", 1: "King", 2: "Queen", 3: "Bishop", 4: "Knight", 5: "Rook"}
        print("Loading capture animations")
        for i in range(0, 6):
            for ii in range(0, 6):
                BVideoFile = "captures/" + "B" + AllNames[i] + "K" + AllNames[ii] + ".mkv"
                WVideoFile = "captures/" + "W" + AllNames[i] + "K" + AllNames[ii] + ".mkv"
                # If the file exists then add it to the videos dictionary
                if os.path.isfile(BVideoFile):
                    videosIndex = "B" + AllNames[i] + "K" + AllNames[ii]
                    self.videos[videosIndex] = VideoFileClip(BVideoFile)
                    self.videos[videosIndex].set_fps(24)
                else:
                    print(BVideoFile + " not found")
                if os.path.isfile(WVideoFile):
                    videosIndex = "W" + AllNames[i] + "K" + AllNames[ii]
                    self.videos[videosIndex] = VideoFileClip(WVideoFile)
                    self.videos[videosIndex].set_fps(24)
                else:
                    print(WVideoFile + " not found")

        print("Captures loaded")
        self.showMenuButton()

# Superclass for a piece
class Piece(object):
    PieceName = ""
    PieceColor = ""
    HasAnimation = False

    def __init__(self, square, color, ColorName):
        #self.obj = loader.loadModel(self.model)
        self.obj = Actor(self.model, self.animations)
        self.obj.reparentTo(render)
        self.obj.setColor(color)
        self.obj.setPos(SquarePos(square))
        self.PieceColor = ColorName
        if(ColorName == "B"):
            self.obj.setH(180)

    def runAnimation(self, StartPosition, EndPosition):
        print("No move animation made yet")

# Example animation
#startPosition = SquarePos(self.dragging)
#endPosition = SquarePos(self.hiSq)

#jumpHeight = 1
#moveSpeed = .5
#middlePosition = CenterPos(startPosition, endPosition, jumpHeight)

#movePiece1 = self.pieces[self.dragging].obj.posInterval(moveSpeed, middlePosition, startPos=startPosition)
#movePiece2 = self.pieces[self.dragging].obj.posInterval(moveSpeed, endPosition, startPos=middlePosition)

#moveAnimation = Sequence(movePiece1, movePiece2)

# Classes for each type of chess piece
class Pawn(Piece):
    model = "models/Pawn"
    HasAnimation = True
    animations = {"Jump": "models/Pawn-Jump", "Trot": "models/Pawn-Trot"}
    PieceName = "Pawn"



    def runAnimation(self, StartPosition, EndPosition):
        # Time it takes for something to occur in seconds
        moveTime = .1
        movedY = abs(EndPosition.getY() - StartPosition.getY())
        if movedY == 2:
            self.obj.play("Jump")
            moveTime = 1
        elif movedY == 1:
            self.obj.play("Trot")
            moveTime = 1.4

        movePiece1 = self.obj.posInterval(moveTime, EndPosition, startPos=StartPosition)
        movePiece1.start()

class King(Piece):
    model = "models/king"
    animations = {}
    PieceName = "King"

class Queen(Piece):
    model = "models/Queen"
    HasAnimation = True
    animations = {"Jump": "models/Queen-Jump"}
    PieceName = "Queen"

    def runAnimation(self, StartPosition, EndPosition):
        #self.obj.play("Forward")
        moveSpeed = .2
        movePiece1 = self.obj.posInterval(moveSpeed, EndPosition, startPos=StartPosition)
        movePiece1.start()

class Bishop(Piece):
    model = "models/bishop"
    animations = {}
    PieceName = "Bishop"

class Knight(Piece):
    model = "models/knight"
    animations = {}
    PieceName = "Knight"

class Rook(Piece):
    model = "models/Rook"
    animations = {"Curl_Up": "models/Rook-Curl_Up", "Curl_Out": "models/Rook-Curl_Out"}
    HasAnimation = True
    PieceName = "Rook"

    def runAnimation(self, StartPosition, EndPosition):
        moveSpeed = 1
        pausePiece = self.obj.posInterval(.1, StartPosition, startPos=StartPosition)
        movePiece1 = self.obj.posInterval(moveSpeed, EndPosition, startPos=StartPosition)
        Start_Curl = self.obj.actorInterval("Curl_Up")
        End_Curl = self.obj.actorInterval("Curl_Out")
        Seq = Sequence(pausePiece, Start_Curl, Wait(.1), movePiece1, End_Curl)
        Seq.start()