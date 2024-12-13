# MyInfiniteCanvas
python script and demo data for infinite canvas painting.

## Usage hint
Start painting and zoom out. When zooming far smaller then the initial zoom level the quality drops, but zooming out works more or less infinite as well as moving.  
There is a simple example already saved in drawing.json. When you start it first time just load the example and zoom out to get an idea about this app.

## New HTML / JS version
Just open MyInfiniteCanvas.html with any browser. Usable on Touchdevices as well.

## Old python installation and start
1. Install python 3.11 (look that up and do it on your prefered way)
2. Install pygame 
   ```
   pip install pygame==2.6.1
   pip install pygame_gui-0.6.12
   ```
4. Run it
   ```python main.py```

## Controls
- Mouse left click - Draw
- Mouse wheel - Zoom
- Arrow Keys - Camera Movement
- S Key - Save
- L Key - Load
- C Key - Color Picker
- I Key - Auto Zoom In
- O key - Auto Zoom Out

## Disclaimer
The python and html / js code were generated fully by perplexity. Only very detailed instructions and bug reports were given to come to this result. Creating this app can be treated as an experiment itself.  
It is used as an proof of concept and to learn more about limitations of perplexity. When I first asked perplexity to create an infinite canvas for infinite zoom and drawing point based, it produced not working code at all, that was not only buggy, but was written in a way, that it could never work.  
Use at your own risk, all liability excluded.
