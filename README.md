# 🌐 Web Scraping and Data Processing Project 🚀

![Version](https://img.shields.io/badge/version-1.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Overview

This project provides a robust solution for scraping web data and processing it efficiently. It uses a blend of requests for multi-threaded data fetching and playwright for dynamic interactions with web pages, making it ideal for handling complex scraping tasks. The data processing part is finely tuned to work with large datasets efficiently, providing quick insights and outputs in various formats.

## 🌟 Features

- Dynamic Web Scraping: Utilizes playwright to interact with JavaScript-heavy websites dynamically.
- Multi-threaded Requests: Employs requests library in a multi-threaded setup to speed up the data fetching process.
- Efficient Data Processing: Leverages pandas and numpy for data cleaning, manipulation, and aggregation.
- Automated Data Collection: Scripts that automate the collection of data periodically, ensuring fresh data is always available.
- Customizable Outputs: Provides functionality to export data into CSV, JSON, or directly into databases.

## 🔧 Installation

```bash
git clone https://github.com/yourusername/projectname.git
cd projectname
pip install -r requirements.txt
```

## 🚀 Usage

To run the script with default settings:
```bash
python main.py
```
To customize the scraping and processing:
```bash
python main.py --days 10 --pages https://www.tiktok.com/@infinityhoop https://www.tiktok.com/@anotherpage --target_eye 50 20000 150 600000 700 --target_star 30 10000 200 300000 400
```
- --days: Number of days to fetch data for (default: 7).
- --pages: TikTok pages to scrape.
- --target_eye & --target_star: Set targets for different metrics like Posts, Likes, Comments, Plays, and Saves.

## 🎨 How It Works

1. Initialization: Set up the URLs and parameters for the scraping.
2. Web Scraping:
   - playwright: Handles dynamic pages, simulating user interactions to fetch data rendered by JavaScript.
   - requests: Manages multiple threads to fetch data from API endpoints or simpler HTML pages.
3. Data Processing:
   - Data is processed and transformed using pandas, with the results being saved into a detailed Google Sheet, which includes comprehensive analytics on emoji usage, engagement metrics, and more.
4. Output:
   - The final output is a Google Sheet which provides a granular view of data metrics by emoji, showing both actual values and predefined targets.

## Output

The script generates a comprehensive `Final.xlsx` file that includes several sheets, each dedicated to different types of emoji-related data metrics such as Likes, Comments, Plays, and Saves. Each sheet not only provides detailed figures but also comparative graphs that illustrate actual values against predetermined targets for both "Eye" and "Star" emojis:

- **Data Sheet**: Raw data collected from TikTok.
- **Emoji Summary**: Frequency of each emoji.
- **Likes Summary**: Total likes per emoji and comparison to target.
- **Comments Summary**: Total comments per emoji and comparison to target.
- **Plays Summary**: Total video plays per emoji and comparison to target.
- **Saves Summary**: Total saves per emoji and comparison to target.

Each summary sheet includes a graph that visually compares the actual values with the target values set for the project, providing immediate insights into performance against goals.

Below are visual representations of the data processed:

![Emoji Frequency Graph](/path/to/emoji_frequency_graph.png)
*Emoji Frequency Graph: This graph shows the frequency of each emoji used in the posts.*

![Likes Comparison Graph](/path/to/likes_comparison_graph.png)
*Likes Comparison Graph: This graph compares actual likes to target likes for each emoji.*

![Comments Comparison Graph](/path/to/comments_comparison_graph.png)
*Comments Comparison Graph: This graph displays actual versus target comments by emoji.*

![Plays Comparison Graph](/path/to/plays_comparison_graph.png)
*Plays Comparison Graph: Visual comparison of actual plays versus target plays for each emoji.*

![Saves Comparison Graph](/path/to/saves_comparison_graph.png)
*Saves Comparison Graph: This chart shows the comparison of actual saves against the target saves for each emoji.*

These visualizations provide a quick overview of the performance metrics and goal attainment across different interaction types on TikTok.

## 📦 Dependencies

- Python 3.10
- pandas
- numpy
- playwright
- requests

## 🤝 Contributing

Contributions are welcome! Please read the contributing guide to learn how to contribute to our project.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎉 Acknowledgments

- Thanks to all the contributors who have helped to build and refine this project.
- Special thanks to open-source projects that made this software possible.

<br><br>

<div align="center">
<div align="center"><p align="center">
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="mhmmdbdrhmd@gmail.com" style="text-decoration: none;" alt="Email">
        <img src="https://github.com/mhmmdbdrhmd/Data/blob/main/Icons/ICON%20_Black%20-%20GMail.png" width="6%" />
    </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/mhmmdbdrhmd" style="text-decoration: none;" alt="GitHub">
        <img src="https://github.com/mhmmdbdrhmd/Data/blob/main/Icons/ICON%20_Black-%20Github.png" width="6%" />
    </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://www.linkedin.com/in/mohamad-badri-ahmadi-aa2a1a8a?original_referer=https%3A%2F%2Fwww.google.com%2F" style="text-decoration: none;" alt="LinkedIn">
        <img src="https://github.com/mhmmdbdrhmd/Data/blob/main/Icons/ICON%20_Black%20-%20Linkding.png" width="6%" />
    </a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <a href="https://twitter.com/mhmmdbdrhmd" style="text-decoration: none;" alt="Twitter">
        <img src="https://github.com/mhmmdbdrhmd/Data/blob/main/Icons/ICON%20_Black%20-%20Twitter%20X.png" width="6%"/>
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
</div>
</div>
