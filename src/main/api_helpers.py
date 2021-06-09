import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
import random
from time import sleep
from tqdm import tqdm


def get_retry() -> Retry:
    """
    Get retry object.

    Parameters
    ----------
    None

    Returns
    -------
    Retry
        Returns a urllib3.util.retry.Retry object        
    """

    #create a retry object
    retries = Retry(total=5,
                    backoff_factor=0.1,
                    status_forcelist=[500, 502, 503, 504])

    return retries


def download_image(url: str = None) -> bytes:
    """
    Download image from url.

    Parameters
    ----------
    url : str
        URL to download from

    Returns
    -------
    bytes
        Returns an image as a bytes object
    """

    #create retry object and start a session
    retries = get_retry()
    s = requests.Session()
    #mount httpadapter to use retry object
    s.mount('http://', HTTPAdapter(max_retries=retries))
    #send a get request and parse the content
    r = s.get(url)
    if r.status_code == 200:
        i = r.content
        return i
    else:
        raise Exception("Failed to pull image!")


def get_random_comics(n: int = 15) -> list[tuple]:
    """
    Get 15 random comics from the xkcd api.

    Parameters
    ----------
    n : int
        Number of random comics to pull. Should be < 81.

    Returns
    -------
    list[tuple]
        Returns a list of comics as tuples

    Examples
    --------
    >>> get_random_comics()
    [(1, 'Kepler', 'Science joke.  You should probably just move along.', 'link': 'https://xkcd.com/21',
    b'xx...', 'https://imgs.xkcd.com/comics/kepler.jpg')]
    """

    #raise error if n > 81
    if n > 88:
        raise ValueError("Value of n should be < 88.")

    #generate a sorted list of random numbers between 1 and 81
    rn_nums = sorted(random.sample(range(1, 88), n))
    #list object to hold the comics data
    comic_l = []
    #define a general endpoint which can be formatted
    api_endpoint = r"https://xkcd.com/{comic_id}/info.0.json"
    link_endpoint = r"https://xkcd.com/"
    #create retry object and start session
    retries = get_retry()
    s = requests.Session()
    #mount httpadapter to use retry
    s.mount('http://', HTTPAdapter(max_retries=retries))
    try:
        for i in tqdm(rn_nums):
            #generate endpoint for a comic with if and send a get request.
            api_endpoint_c = api_endpoint.format(comic_id=i)
            r = s.get(api_endpoint_c)
            #parse the reponse data and create dictionaries to store comics data
            comic_j = r.json()
            image = download_image(comic_j["img"])
            link = link_endpoint + str(comic_j["num"])
            comic_t = (str(comic_j["num"]), comic_j["title"], comic_j["alt"],
                       link, image, comic_j["img"], str(comic_j["num"]))
            comic_l.append(comic_t)
            #be mindfull of using free apis by avoiding burst of requests
            sleep(0.1)
    except Exception as e:
        print(e)
    return comic_l
