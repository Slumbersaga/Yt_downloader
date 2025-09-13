# yt-dlp GUI

This project provides a graphical user interface (GUI) for the yt-dlp package, allowing users to easily download videos from various platforms.

## Features

- User-friendly, modern interface for downloading videos.
- Input fields for video URLs with clipboard paste support.
- Fetches and displays video information (title, duration, uploader, thumbnail, etc.).
- Selectable resolution and output format (MP4, MP3, WebM).
- Progress tracking with ETA and elapsed time.
- Download history with quick access to downloaded files.
- Error handling and validation for URLs.
- Tooltips for better usability.

## Requirements

To run this project, you need to have Python installed (version 3.7 or higher recommended) along with the following dependencies:

- **yt-dlp**: The core video downloading library.
- **Pillow**: For displaying video thumbnails in the GUI.
- **requests**: For fetching video thumbnails from the web.
- **tkinter**: Standard Python GUI library (comes pre-installed with most Python distributions).

You can install the required packages using:

```
pip install yt-dlp pillow requests
```

> **Note:**  
> `tkinter` is included with most Python installations. If you encounter issues, install it via your OS package manager (e.g., `sudo apt-get install python3-tk` on Ubuntu).

## Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yourusername/yt-dlp-gui.git
   cd yt-dlp-gui
   ```

2. **Install the required packages:**
   ```
   pip install yt-dlp pillow requests
   ```

## Usage

1. **Run the application:**
   ```
   python src/gui.py
   ```
   to run the file you have to write this in the command line after navigating to the src file
   ```
   python gui.py
   ```

2. **How to use:**
   - Enter or paste the video URL in the input field.
   - Click "Fetch Info" to preview video details.
   - Select the desired resolution and format.
   - Choose the output folder if needed.
   - Click "Download" to start downloading.
   - Monitor the progress bar and status messages.
   - Access recent downloads from the history list.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.