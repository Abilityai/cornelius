---
created: '2026-01-10'
updated: '2026-03-03'
tags:
- anytype-import
- project
type: permanent
source_type: project
anytype_id: bafyreiasgcklaed5omngtl7ehwhbj5cz3xg4lgicz3s4hjhgvluqaewk54
created_by: human
updated_by: claude-opus-4-6
agent_version: '02.25'
local_path: /Users/jlb/Documents/Projects/Inflection/inflection-image-processor
status: Done
---
# inflection-image-processor   
# Image Inflection Processor   
## Description   
Image Inflection Processor is a command-line tool that applies an inflection effect to images. It processes input images by dividing them into a grid and replacing each cell with a pattern SVG, where the size and type of pattern are determined by the brightness of the corresponding area in the original image.   
## Features   
- Process images with customizable resolution   
- Apply unique SVG patterns based on image brightness   
- Output processed images in PNG format   
   
## Example   
Input Image:
   
Output Image (resolution 50):
   
Output Image (resolution 100):
   
## Installation   
1. Clone the repository:   
    ```
    git clone https://github.com/inflectionxyz/inflection-image-processor.git
    cd inflection-image-processor
    
    ```
    or   
    ```
    gh repo clone https://github.com/inflectionxyz/inflection-image-processor.git
    cd inflection-image-processor
    
    ```
2. Install dependencies:   
    ```
    npm install
    
    ```
3. Build the project:   
    ```
    npm run build
    
    ```
4. Link the CLI tool:   
    ```
    npm link
    
    ```
   
## Usage   
Run the tool using the following command:   
```
iip <input-image-path> -r <resolution> -w <output-width> -h <output-height>

```
Required Parameters:   
- : Path to the input image file   
   
Optional Parameters:   
- -r, --resolution : Number of cells along the width of the image (e.g., 25, 50, 100) (default: 25% of image width)   
- -w, --output-width : Desired width of the output image (default: original image width)   
- -h, --output-height : Desired height of the output image (default: original height width)   
   
Resizing Behavior:   
If neither output-width nor output-height is provided, the original image dimensions are used.
If either output-width or output-height is provided, the image is scaled proportionally to cover that dimension.
If both output-width and output-height are provided, the image is scaled to cover the bounding box defined by these dimensions, maintaining aspect ratio. The image is then center-cropped to fit exactly.   
Example:   
```
iip path/to/your/image.jpg -r 50

```
The processed image will be saved in the same directory as the input image with "\_inflection" appended to the filename.   
## Requirements   
- Node.js (I'm using v20)   
