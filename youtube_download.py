import os.path
from fake_useragent import UserAgent
from pytube.exceptions import RegexMatchError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from pytube import YouTube
import pathlib


def chrome_browser():
    opt = Options()
    ser = Service(ChromeDriverManager().install())
    """
    disable headless, enable detach when debugging
    """
    #opt.add_argument('--headless')
    opt.add_experimental_option("detach", True)

    #user_agent = UserAgent()  # random header info
    #opt.add_argument('--user-agent=%s' % user_agent.random)
    opt.add_argument('--disable-gpu')
    opt.add_experimental_option("excludeSwitches", ["enable-logging"])
    opt.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(service=ser, options=opt)


def search(url, max_retry=5):
    title_href = ""
    retry = 0
    while max_retry+1 > retry:
        browser = chrome_browser()
        try:
            browser.get(url)
            WebDriverWait(browser, 20, 5).until(ec.presence_of_element_located((By.ID, 'video-title')))
        except:

            print("error loading page, retrying...")
            retry += 1
            browser.quit()
            continue
        try:
            tags = browser.find_elements(By.TAG_NAME, "a")
        except:
            print("error no a-tags found")
            retry += 1
            continue
        for tag in tags:
            href = tag.get_attribute('href')
            if 'watch' in str(href):
                title = tag.get_attribute('title')
                if title == '':
                    try:
                        title = tag.find_element(By.ID, 'video-title').get_attribute('title')
                    except:
                        pass
                if title != '':
                    title_href = f'{title} href={href}'
                    break
        if title_href == "":
            print("title_href is empty, retrying...")
            browser.quit()
            retry += 1
        else:
            print("search complete!")
            break
    browser.quit()
    return title_href


def download(title_href, file_format, output_path):
    print("initiate download...")
    if title_href is None:
        return "something went wrong, title and href not found"
    title, href = title_href.split(" href=")
    file_name = title.replace("\\", "").replace("/", "_").replace(":", "_").replace("*", "") \
        .replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "").replace(' ', '')
    yt = YouTube(href)
    file_w_extension = f'{file_name}.{file_format.lower()}'
    if file_format == 'MP3':
        yt.streams.filter()\
            .get_audio_only()\
            .download(output_path=output_path, filename=file_w_extension)
    elif file_format == 'MP4':
        yt.streams.filter(progressive=True, file_extension='mp4')\
            .order_by('resolution')\
            .desc()\
            .first()\
            .download(output_path=output_path, filename=file_w_extension)
    else:
        print("something went wrong, not valid file format (MP3 or MP4)")
    return file_w_extension


# def get_ytd(youtube_url, file_format):
#     search_url = f"https://www.youtube.com/results?search_query={youtube_url}"
#     file_format = file_format.rstrip()
#     output_path = os.path.join(pathlib.Path().resolve(), "mp3/").replace("\\", "/")
#     try:
#         file_name = download(search(search_url), file_format, output_path)
#         if not file_name == "":
#             print("download finished!")
#         file_full_path = os.path.join(output_path, file_name)
#         print(file_full_path)
#         return file_full_path
#     except Exception as e:
#         print("error\nmessage:\n", e)
#         return ""


def get_yt(youtube_url, file_format):
    try:
        yt = YouTube(youtube_url)
    except RegexMatchError as e:
        print(e)
        return
    except Exception as e:
        print(e)
        return
    file_format = file_format.rstrip().lower()
    output_path = os.path.join(pathlib.Path().resolve(), f"{file_format}/").replace("\\", "/")

    file_name = yt.title.replace("\\", "").replace("/", "_").replace(":", "_").replace("*", "") \
        .replace("?", "").replace("\"", "").replace("<", "").replace(">", "").replace("|", "--").replace(' ', '-')
    file_w_extension = f'{file_name}.{file_format}'
    if file_format == 'mp3':
        yt.streams.filter() \
            .get_audio_only() \
            .download(output_path=output_path, filename=file_w_extension)
    elif file_format == 'mp4':
        yt.streams.filter(progressive=True, file_extension='mp4') \
            .order_by('resolution') \
            .desc() \
            .first() \
            .download(output_path=output_path, filename=file_w_extension)
    else:
        print("something went wrong, not valid file format (MP3 or MP4)")
    file_full_path = os.path.join(output_path, file_w_extension)
    print(file_full_path)
    return file_full_path


"""
debug pytube function
"""
# if __name__ == '__main__':
#     try:
#         get_yt('https://youtu.be/9zM-dnqQ5ss', 'MP4')
#     except RegexMatchError as e:
#         print(e)
#     except Exception as e:
#         print(e)



# attempt using subprocess to no avail
# if __name__ == '__main__':
# youtubeUrl = "https://www.youtube.com/watch?v=Hu3Q9t6H4yw"
# searchUrl = f"https://www.youtube.com/results?search_query={youtubeUrl}"

# from shell
# arg1 = sys.argv[1]
# arg2 = sys.argv[2].rstrip()
# searchUrl = f"https://www.youtube.com/results?search_query={arg1}"
# fileFormat = arg2
#
# # fileFormat = 'MP3'
# # fileFormat = 'MP4'
# outputPath = os.path.join(pathlib.Path().resolve(), "mp3/").replace("\\", "/")
# try:
#     file_name = download(search(chrome_browser(), searchUrl), fileFormat, outputPath)
#     print("download finished!")
#     file_full_path = os.path.join(outputPath, file_name)
#     print(file_full_path)
# except Exception as e:
#     print("error\nmessage:\n", e)
