import hashlib
import datetime
import os
import json
from concurrent.futures import ThreadPoolExecutor
import requests
from time import sleep
import asyncio
from bs4 import BeautifulSoup
from lxml import html
import asyncio
from playwright.async_api import async_playwright
import random
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import json
from time import sleep
import re
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import os
import json
import pandas as pd 
import emoji
import shutil
import argparse
import datetime
import warnings



def clear_tmp_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and all its contents
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def load_data_from_folder(folder_path):
    data = []  # List to hold all data dicts
    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):  # Check if the file is a JSON file
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                # Load data from JSON file and add to list
                data.append(json.load(file))
    return data

def extract_first_emoji(text):
    for char in text:
        if char in emoji.UNICODE_EMOJI['en']:  # Check if the character is an emoji
            return char
    return None  # Return None if no emoji is found

def map_emojis_to_identifiers(df, emoji_column):
    # Count the occurrences of each emoji
    emoji_counts = df[emoji_column].value_counts().to_dict()
    
    # Sort emojis by their frequency (most frequent first), breaking ties alphabetically
    sorted_emojis = sorted(emoji_counts, key=lambda x: (-emoji_counts[x], x))
    
    # Map each emoji to a unique identifier starting from 0
    emoji_to_id = {emo: i for i, emo in enumerate(sorted_emojis) if emo is not None}
    emoji_to_id[None] = 0  # Assign 0 to descriptions without emojis
    
    return df[emoji_column].map(emoji_to_id), emoji_to_id  # Return a Series mapping emojis to identifiers

def data_to_spreadsheet(folder_path, output_filename,targets):
    print("Processing...")
    # Load the data from the specified folder
    data = load_data_from_folder(folder_path)
    
    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(data)

    df['First Emoji'] = df['description'].apply(extract_first_emoji)

    # Filter DataFrame for rows where First Emoji is either an eye or a star
    eye_emoji = '👀'  # Make sure this is the correct eye emoji you're looking for
    star_emoji = '✨'
    df = df[df['First Emoji'].isin([eye_emoji, star_emoji])]

    # Map emojis to unique identifiers and add a new column
    df['Emoji Identifier'],emoji_to_identifier = map_emojis_to_identifiers(df, 'First Emoji')
    target_data = {'eye': targets[0], 'star': targets[1]}

    # Map emojis to identifiers
    emoji_to_identifier2 = {
        '👀': 'eye',
        '✨': 'star'
    }





    # Load the updated DataFrame





    # Apply the function to the 'description' column
    df['First Emoji'] = df['description'].apply(extract_first_emoji)

    # Count the occurrences of each emoji and sort them by frequency
    emoji_frequencies = df['First Emoji'].value_counts().sort_values(ascending=False)

    # Create a dictionary to map emojis to identifiers based on frequency
    #emoji_to_identifier = {emoji: index for index, emoji in enumerate(emoji_frequencies.index)}



    # Map each emoji in the 'First Emoji' column to its identifier
    df['Emoji Identifier'] = df['First Emoji'].map(emoji_to_identifier)

    df['Target'] = df['First Emoji'].map(emoji_to_identifier2).map(target_data)
    target_columns = ['Target Posts', 'Target Likes', 'Target Comments', 'Target Plays', 'Target Saves']
    df[target_columns] = pd.DataFrame(df['Target'].tolist(), index=df.index)



    # Now we have a DataFrame with the original data plus the 'First Emoji' and 'Emoji Identifier' columns
    # Next, we create a bar chart of emoji frequencies

    # Create a summary DataFrame for the bar chart
    post_summary = emoji_frequencies.reset_index()
    post_summary.columns = ['Emoji', 'Frequency']
    post_summary['Target'] = post_summary['Emoji'].map(emoji_to_identifier2).map(lambda x: target_data[x][0])

    df['Likes'] = pd.to_numeric(df['Likes'], errors='coerce').fillna(0)
    df['Comments'] = pd.to_numeric(df['Comments'], errors='coerce').fillna(0)
    df['Plays'] = pd.to_numeric(df['Plays'], errors='coerce').fillna(0)
    df['Saves'] = pd.to_numeric(df['Saves'], errors='coerce').fillna(0)

    # Sum the 'Likes' for each 'First Emoji'
    likes_sum = df.groupby('First Emoji')['Likes'].sum().sort_values(ascending=False).reset_index()
    likes_sum.columns = ['Emoji', 'Total Likes']
    likes_sum['Target'] = likes_sum['Emoji'].map(emoji_to_identifier2).map(lambda x: target_data[x][1])

    comments_sum = df.groupby('First Emoji')['Comments'].sum().sort_values(ascending=False).reset_index()
    comments_sum.columns = ['Emoji', 'Total Comments']
    comments_sum['Target'] = comments_sum['Emoji'].map(emoji_to_identifier2).map(lambda x: target_data[x][2])

    plays_sum = df.groupby('First Emoji')['Plays'].sum().sort_values(ascending=False).reset_index()
    plays_sum.columns = ['Emoji', 'Total Plays']
    plays_sum['Target'] = plays_sum['Emoji'].map(emoji_to_identifier2).map(lambda x: target_data[x][3])

    saves_sum = df.groupby('First Emoji')['Saves'].sum().sort_values(ascending=False).reset_index()
    saves_sum.columns = ['Emoji', 'Total Saves']
    saves_sum['Target'] = saves_sum['Emoji'].map(emoji_to_identifier2).map(lambda x: target_data[x][4])



    # Save the summary DataFrame to a new Excel file and create the bar chart
    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Data')
        post_summary.to_excel(writer, index=False, sheet_name='Post Summary')

        # Access the XlsxWriter objects
        workbook = writer.book
        worksheet = writer.sheets['Post Summary']
        post_chart = workbook.add_chart({'type': 'column'})

        # Configure the chart series
        post_chart.add_series({
            'categories': '=Post Summary!$A$2:$A${}'.format(len(post_summary) + 1),
            'values': '=Post Summary!$B$2:$B${}'.format(len(post_summary) + 1),
            'name': 'Total Posts',
        })

        # Configure the chart title and axis labels
        post_chart.set_title({'name': 'Posts'})
        post_chart.set_x_axis({'name': 'Emojis'})
        post_chart.set_y_axis({'name': 'Total Posts'})

        # Insert the chart into the worksheet
        worksheet.insert_chart('D2', post_chart)



        post_chart_v2 = workbook.add_chart({'type': 'column', 'subtype': 'clustered'})

        # Configure the chart by adding the series for actual and target values
        # Assuming 'B' column has the actual values and 'C' column has the target values
        post_chart_v2.add_series({
            'name':       'Actual',
            'categories': '=Post Summary!$A$2:$A${}'.format(len(post_summary) + 1),
            'values':     '=Post Summary!$B$2:$B${}'.format(len(post_summary) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })
        post_chart_v2.add_series({
            'name':       'Target',
            'categories': '=Post Summary!$A$2:$A${}'.format(len(post_summary) + 1),
            'values':     '=Post Summary!$C$2:$C${}'.format(len(post_summary) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })

        # Configure the chart titles and axes
        post_chart_v2.set_title({'name': 'Comparison of Total Posts and Targets by Emoji'})
        post_chart_v2.set_x_axis({'name': 'Emojis'})
        post_chart_v2.set_y_axis({'name': 'Total Posts'})

        # Optionally, set the style of the chart
        post_chart_v2.set_style(11)  # Use predefined chart style 11

        # Insert the chart into the worksheet
        worksheet.insert_chart('L2', post_chart_v2)
        


        # Write the emoji_likes_sum DataFrame
        likes_sum.to_excel(writer, index=False, sheet_name='Likes Summary')

        # Access the XlsxWriter workbook and worksheet objects for the new chart
        likes_worksheet = writer.sheets['Likes Summary']
        likes_chart = workbook.add_chart({'type': 'column'})

        # Configure the series for the likes chart
        likes_chart.add_series({
            'categories': '=Likes Summary!$A$2:$A${}'.format(len(likes_sum) + 1),
            'values':     '=Likes Summary!$B$2:$B${}'.format(len(likes_sum) + 1),
            'name':       'Total Likes',
        })

        # Configure the likes chart title and axis labels
        likes_chart.set_title({'name': 'Total Likes by Emoji'})
        likes_chart.set_x_axis({'name': 'Emojis'})
        likes_chart.set_y_axis({'name': 'Total Likes'})

        # Insert the likes chart into the worksheet
        likes_worksheet.insert_chart('D2', likes_chart)

        likes_chart_v2 = workbook.add_chart({'type': 'column', 'subtype': 'clustered'})

        # Configure the chart by adding the series for actual and target values
        # Assuming 'B' column has the actual values and 'C' column has the target values
        likes_chart_v2.add_series({
            'name':       'Actual',
            'categories': '=Likes Summary!$A$2:$A${}'.format(len(likes_sum) + 1),
            'values':     '=Likes Summary!$B$2:$B${}'.format(len(likes_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })
        likes_chart_v2.add_series({
            'name':       'Target',
            'categories': '=Likes Summary!$A$2:$A${}'.format(len(likes_sum) + 1),
            'values':     '=Likes Summary!$C$2:$C${}'.format(len(likes_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })

        # Configure the chart titles and axes
        likes_chart_v2.set_title({'name': 'Comparison of Total Likes and Targets by Emoji'})
        likes_chart_v2.set_x_axis({'name': 'Emojis'})
        likes_chart_v2.set_y_axis({'name': 'Total Likes'})

        # Optionally, set the style of the chart
        likes_chart_v2.set_style(11)  # Use predefined chart style 11

        # Insert the chart into the worksheet
        likes_worksheet.insert_chart('L2', likes_chart_v2)


        
        comments_sum.to_excel(writer, index=False, sheet_name='Comments Summary')

        # Access the XlsxWriter workbook and worksheet objects for the new chart
        comments_worksheet = writer.sheets['Comments Summary']
        comments_chart = workbook.add_chart({'type': 'column'})

        # Configure the series for the likes chart
        comments_chart.add_series({
            'categories': '=Comments Summary!$A$2:$A${}'.format(len(comments_sum) + 1),
            'values':     '=Comments Summary!$B$2:$B${}'.format(len(comments_sum) + 1),
            'name':       'Total Comments',
        })

        # Configure the likes chart title and axis labels
        comments_chart.set_title({'name': 'Total Comments by Emoji'})
        comments_chart.set_x_axis({'name': 'Emojis'})
        comments_chart.set_y_axis({'name': 'Total Comments'})

        # Insert the likes chart into the worksheet
        comments_worksheet.insert_chart('D2', comments_chart)


        comments_chart_v2 = workbook.add_chart({'type': 'column', 'subtype': 'clustered'})

        # Configure the chart by adding the series for actual and target values
        # Assuming 'B' column has the actual values and 'C' column has the target values
        comments_chart_v2.add_series({
            'name':       'Actual',
            'categories': '=Comments Summary!$A$2:$A${}'.format(len(comments_sum) + 1),
            'values':     '=Comments Summary!$B$2:$B${}'.format(len(comments_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })
        comments_chart_v2.add_series({
            'name':       'Target',
            'categories': '=Comments Summary!$A$2:$A${}'.format(len(comments_sum) + 1),
            'values':     '=Comments Summary!$C$2:$C${}'.format(len(comments_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })

        # Configure the chart titles and axes
        comments_chart_v2.set_title({'name': 'Comparison of Total Comments and Targets by Emoji'})
        comments_chart_v2.set_x_axis({'name': 'Emojis'})
        comments_chart_v2.set_y_axis({'name': 'Total Comments'})

        # Optionally, set the style of the chart
        comments_chart_v2.set_style(11)  # Use predefined chart style 11

        # Insert the chart into the worksheet
        comments_worksheet.insert_chart('L2', comments_chart_v2)



        
        plays_sum.to_excel(writer, index=False, sheet_name='Plays Summary')

        # Access the XlsxWriter workbook and worksheet objects for the new chart
        plays_worksheet = writer.sheets['Plays Summary']
        plays_chart = workbook.add_chart({'type': 'column'})

        # Configure the series for the likes chart
        plays_chart.add_series({
            'categories': '=Plays Summary!$A$2:$A${}'.format(len(plays_sum) + 1),
            'values':     '=Plays Summary!$B$2:$B${}'.format(len(plays_sum) + 1),
            'name':       'Total Plays',
        })

        # Configure the likes chart title and axis labels
        plays_chart.set_title({'name': 'Total Plays by Emoji'})
        plays_chart.set_x_axis({'name': 'Emojis'})
        plays_chart.set_y_axis({'name': 'Total Plays'})

        # Insert the likes chart into the worksheet
        plays_worksheet.insert_chart('D2', plays_chart)


        plays_chart_v2 = workbook.add_chart({'type': 'column', 'subtype': 'clustered'})

        # Configure the chart by adding the series for actual and target values
        # Assuming 'B' column has the actual values and 'C' column has the target values
        plays_chart_v2.add_series({
            'name':       'Actual',
            'categories': '=Plays Summary!$A$2:$A${}'.format(len(plays_sum) + 1),
            'values':     '=Plays Summary!$B$2:$B${}'.format(len(plays_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })
        plays_chart_v2.add_series({
            'name':       'Target',
            'categories': '=Plays Summary!$A$2:$A${}'.format(len(plays_sum) + 1),
            'values':     '=Plays Summary!$C$2:$C${}'.format(len(plays_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })

        # Configure the chart titles and axes
        plays_chart_v2.set_title({'name': 'Comparison of Total Plays and Targets by Emoji'})
        plays_chart_v2.set_x_axis({'name': 'Emojis'})
        plays_chart_v2.set_y_axis({'name': 'Total Plays'})

        # Optionally, set the style of the chart
        plays_chart_v2.set_style(11)  # Use predefined chart style 11

        # Insert the chart into the worksheet
        plays_worksheet.insert_chart('L2', plays_chart_v2)



        #######################
        saves_sum.to_excel(writer, index=False, sheet_name='Saves Summary')

        # Access the XlsxWriter workbook and worksheet objects for the new chart
        saves_worksheet = writer.sheets['Saves Summary']
        saves_chart = workbook.add_chart({'type': 'column'})

        # Configure the series for the likes chart
        saves_chart.add_series({
            'categories': '=Saves Summary!$A$2:$A${}'.format(len(saves_sum) + 1),
            'values':     '=Saves Summary!$B$2:$B${}'.format(len(saves_sum) + 1),
            'name':       'Total Saves',
        })

        # Configure the likes chart title and axis labels
        saves_chart.set_title({'name': 'Total Saves by Emoji'})
        saves_chart.set_x_axis({'name': 'Emojis'})
        saves_chart.set_y_axis({'name': 'Total Saves'})

        # Insert the likes chart into the worksheet
        saves_worksheet.insert_chart('D2', saves_chart)

        saves_chart_v2 = workbook.add_chart({'type': 'column', 'subtype': 'clustered'})

        # Configure the chart by adding the series for actual and target values
        # Assuming 'B' column has the actual values and 'C' column has the target values
        saves_chart_v2.add_series({
            'name':       'Actual',
            'categories': '=Saves Summary!$A$2:$A${}'.format(len(saves_sum) + 1),
            'values':     '=Saves Summary!$B$2:$B${}'.format(len(saves_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })
        saves_chart_v2.add_series({
            'name':       'Target',
            'categories': '=Saves Summary!$A$2:$A${}'.format(len(saves_sum) + 1),
            'values':     '=Saves Summary!$C$2:$C${}'.format(len(saves_sum) + 1),
            'data_labels': {'value': True, 'position': 'inside_end'},  # Show data labels
        })

        # Configure the chart titles and axes
        saves_chart_v2.set_title({'name': 'Comparison of Total Saves and Targets by Emoji'})
        saves_chart_v2.set_x_axis({'name': 'Emojis'})
        saves_chart_v2.set_y_axis({'name': 'Total Saves'})

        # Optionally, set the style of the chart
        saves_chart_v2.set_style(11)  # Use predefined chart style 11

        # Insert the chart into the worksheet
        saves_worksheet.insert_chart('L2', saves_chart_v2)




        

    # The file is saved automatically when the 'with' block is exited
    print("Updated Excel file with chart saved.")


def tiktok_id_to_timestamp(tiktok_url):
    # Extract the video ID from the URL
    video_id = tiktok_url.split('/')[-1] if '/' in tiktok_url else tiktok_url
    
    try:
        # Convert the video ID to an integer
        video_id_num = int(video_id)
        
        # Shift the bits to get the timestamp
        timestamp = video_id_num >> 32
        
        # Convert timestamp to human-readable format
        date_time = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        return f"{date_time}"
    except ValueError:
        return "Invalid TikTok video ID or URL."
    except OverflowError:
        return "Timestamp conversion error due to number size."



def safe_filename(tiktok_url):
    """Generate a hash of the URL to create a safe filename."""
    return tiktok_url.split('/')[-1] if '/' in tiktok_url else tiktok_url


async def manual_login(page_urls,end_date):
    print("Fetching Links...")
    end_timestamp = end_date.timestamp()  # convert end_date to a timestamp for comparison
    hrefs = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, args=[
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--disable-dev-shm-usage',
            '--disable-web-security',  # Disable web security - use with caution
            '--disable-features=IsolateOrigins,site-per-process',  # Loosen security (risky)
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',  # This option can help if you're running in a docker container
            '--disable-setuid-sandbox',
            '--disable-webgl',
            '--disable-accelerated-2d-canvas',
            '--disable-images',  # Assume your tool allows disabling images directly
            '--disable-gpu'  # Disabling GPU hardware acceleration
        ])
        '''
        browser = await p.chromium.launch(headless=True, args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-gpu',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--disable-images',  # Assume your tool allows disabling images directly
            '--mute-audio',  # Prevents any audio processing
        ])'''

        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            bypass_csp=True,  # Bypass content security policy
            viewport={'width': 1920, 'height': 1080},  # Set a specific viewport size
            geolocation={'latitude': 37.7749, 'longitude': -122.4194},  # Simulate geolocation
            permissions=['geolocation'],  # Allow geolocation permission
            extra_http_headers={
                'Accept-Language': 'en-US,en;q=0.9'  # Set a common accept-language header
            }
        )
        page = await context.new_page()
        # Set default timeout for all operations to unlimited
        page.set_default_timeout(0)  
        hrefs = []
        page_counter=0
        for page_url in page_urls:
            page_counter+=1
            await page.goto(page_url)


            if page_counter==1:
                
                # Wait indefinitely for an element at a specific XPath to appear
                #await page.wait_for_selector('xpath=/html/body/div[6]/div', state='attached', timeout=0)

                #await page.wait_for_selector('xpath=/html/body/div[6]/div', state='detached', timeout=0)


                #await page.wait_for_selector('button[type="button"]:has-text("Accept all")')
                #await page.click('button[type="button"]:has-text("Accept all")')

                # Wait for and click the "Not now" button if it appears
                await page.wait_for_selector('text="Continue as guest"')
                await page.click('text="Continue as guest"')
                


            #await page.wait_for_timeout(5000)  # Adjust timeout as necessary
            
            last_height = await page.evaluate("document.body.scrollHeight")
        
            # This will count the number of video tags on the page, assuming each video tag represents a post
            initial_items = await page.eval_on_selector_all(".css-x6y88p-DivItemContainerV2", "elements => elements.length")


        
            number_of_scrolls = 0
            found_older = False

            while not found_older:
                new_index = (number_of_scrolls + 1) * initial_items
                await page.wait_for_selector(f".css-x6y88p-DivItemContainerV2:nth-of-type({new_index})");
            
                
                


                # Extract and check the dates of the new posts
                for i in range(new_index - initial_items + 1, new_index + 1):
                    if i >3:
                        try:
                            await page.wait_for_selector(f".css-x6y88p-DivItemContainerV2:nth-of-type({i}) a")
                            href = await page.get_attribute(f".css-x6y88p-DivItemContainerV2:nth-of-type({i}) a" , "href")
                            post_date = tiktok_id_to_timestamp(href)
                            post_timestamp = datetime.datetime.strptime(post_date, '%Y-%m-%d %H:%M:%S').timestamp()

                            if post_timestamp > end_timestamp:
                                hrefs.append(href)
                            else:
                                found_older = True
                                break
                        except Exception as e:
                            # Handle exceptions as needed
                            break

                if not found_older:
                    # Scroll down to load more posts
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    number_of_scrolls += 1
            

        

    return hrefs


def fetch_caption(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        # Add other headers used by curl if necessary
    }

    success = False
    while not success:
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                sleep(1)  # Wait for 1 second before retrying   
            



            response.raise_for_status() 

            pattern = r'{"diggCount":(\d+),"shareCount":(\d+),"commentCount":(\d+),"playCount":(\d+),"collectCount":"(\d+)"}'
            
            # Search for the pattern in the content
            match = re.search(pattern, response.text)
            
            if match:
                data = {
                    'Likes': match.group(1),
                    'Shares': match.group(2),
                    'Comments': match.group(3),
                    'Plays': match.group(4),
                    'Saves': match.group(5)
                }
            else:
                data = {
                    'Likes': "Not Found",
                    'Shares': "Not Found",
                    'Comments': "Not Found",
                    'Plays': "Not Found",
                    'Saves': "Not Found"
                }
                #print(f"No pattern match found in response for URL {url}")
                
            
            
            
            

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Finding the correct script tag
            script_tag = None
            for tag in soup.find_all('script'):
                if 'seo.abtest' in tag.text:
                    script_tag = tag.text
                    break

            if not script_tag:
                return "No JSON data found in the script tags."

            try:
                # Attempt to isolate the JSON data by removing unnecessary parts
                start = script_tag.find('{')
                end = script_tag.rfind('}') + 1
                json_str = script_tag[start:end]

                json_data = json.loads(json_str)

                # Extracting the video description from the JSON data
                description = json_data.get('__DEFAULT_SCOPE__').get('webapp.video-detail', {}).get('itemInfo', {}).get('itemStruct', {}).get('desc', 'No description found')
                data['description'] = description
                success = True
            except json.JSONDecodeError as e:
                #print(f"JSON decoding error: {str(e)}")
                1
            except Exception as e:
                #print(f"Error processing data: {str(e)}")
                1
    
        except requests.exceptions.RequestException as e:
                #print(f"Error fetching {url}: {e}")
                sleep(1)  # Wait for 1 second before retrying

    
    
    data['Date'] = tiktok_id_to_timestamp(url)

    filename = f"{safe_filename(url)}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    
    
    with open(os.path.join('tmp', filename), 'w') as f:
        json.dump(data, f, indent=4)

    
    return data




# Using ThreadPoolExecutor to handle multiple URLs concurrently
def parallel_fetch_caption(urls):
    os.makedirs('tmp', exist_ok=True)
    clear_tmp_folder('tmp')
    with ThreadPoolExecutor(max_workers=70) as executor:
        # Set up future objects for each URL fetch operation
        futures = [executor.submit(fetch_caption, url) for url in urls]
        results = []

        # Use tqdm to create a progress bar for the futures
        for future in tqdm(as_completed(futures), total=len(urls), desc="Fetching data"):
            try:
                result = future.result()  # Get the result of each future
                results.append(result)
            except Exception as e:
                #print(f"An error occurred: {e}")
                1

        return results


#python main.py --days 10 --pages https://www.tiktok.com/@infinityhoop https://www.tiktok.com/@anotherpage --target_eye 50 20000 150 600000 700 --target_star 30 10000 200 300000 400
if __name__ == "__main__":
    # Filter out specific warnings by message
    warnings.filterwarnings("ignore")

    parser = argparse.ArgumentParser(description='Run TikTok data scraping and processing.')
    parser.add_argument('--pages', nargs='+', default=['https://www.tiktok.com/@infinityhoop'],
                        help='List of TikTok pages to scrape')
    parser.add_argument('--days', type=int, default=7,
                        help='Number of days back to scrape')
    parser.add_argument('--target_eye', nargs=5, type=int,
                        default=[40, 10000, 100, 500000, 600],
                        help='Target values for eye emoji: Posts, Likes, Comments, Plays, Saves')
    parser.add_argument('--target_star', nargs=5, type=int,
                        default=[20, 5000, 50, 250000, 300],
                        help='Target values for star emoji: Posts, Likes, Comments, Plays, Saves')

    args = parser.parse_args()

    # Convert number of days to datetime
    end_date = datetime.datetime.now() - datetime.timedelta(days=args.days)

    # Run the scraping and processing functions
    hrefs = asyncio.run(manual_login(args.pages, end_date))
    results = parallel_fetch_caption(hrefs)
    data_to_spreadsheet("tmp", "Final.xlsx", [args.target_eye, args.target_star])





