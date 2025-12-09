# Document Scanner

This project is a document scanner built using OpenCV and Python. It takes an image of a document, detects the document's edges, applies a perspective transform to get a top-down view, and then applies thresholding to give it a scanned look.

## Features

*   **Automatic Document Detection**: Finds the document in the image using edge detection and contour analysis.
*   **Perspective Correction**: Warps the detected document to a flat, top-down view.
*   **Thresholding**: Converts the document to a clean, black and white scanned image.
*   **Inverted Output**: Option to invert the colors of the output.

## Project Structure

```
opencv-project-template/
│
├── src/
│   ├── main.py       # Main application logic
│   └── utils.py      # Helper functions for image processing
│
├── assets/           # Input images
│   └── sample.jpg
│
├── results/          # Processed output images
│   └── corrected.png
│
├── requirements.txt  # Python dependencies
├── README.md         # Project documentation
└── .gitignore
```

## Installation

1.  Clone the repository:
    ```bash
    git clone <your-repo-link>
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the `main.py` script from the root directory:

```bash
python src/main.py --image assets/sample.jpg
```

### Arguments

*   `-i`, `--image`: Path to the input image (Required).
*   `-I`, `--inverted`: Optional flag to invert the output colors.

### Example

```bash
python src/main.py --image assets/receipt.jpg --inverted
```

## Output

The processed images will be saved in the `results/` directory:
*   `corrected.png`: The perspective-corrected image.
*   `thresholded.png` (or `thresholded_inverted.png`): The final scanned output.

