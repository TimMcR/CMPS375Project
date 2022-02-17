import direct.directbase.DirectStart
from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import *
from panda3d.core import TextNode

def setupMenu():

    # Add some text
    bk_text = "This is my Demo"
    menuImage = OnscreenImage(image="images/Chess_Menu_Image.png")

    textObject = OnscreenText(text=bk_text, pos=(0.95,-0.95), scale=0.07,
                              fg=(1, 0.5, 0.5, 1), align=TextNode.ACenter,
                              mayChange=1)

    # Callback function to set  text
    def setText():
            b.destroy()
            menuImage.destroy()
            bk_text = "Button Clicked"
            textObject.setText(bk_text)

    # Add button
    b = DirectButton(text=("OK", "click!", "rolling over", "disabled"),
                     scale=.05, command=setText)