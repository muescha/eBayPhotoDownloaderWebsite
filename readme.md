# eBay Photo Downloader

## Overview

The eBay Photo Downloader is a web application designed to simplify the process of downloading images from eBay listings. By leveraging the power of Flask, a lightweight WSGI web application framework, this app provides a user-friendly interface for users to quickly and easily download all the photos associated with any eBay listing by simply entering the URL of the listing.

## How It Works

1. **Enter eBay Listing URL**: Users start by entering the URL of the eBay listing from which they wish to download images into the provided input field on the home page.

2. **Download Photos**: After submitting the URL, the application processes the request by scraping the listing page for image URLs, downloading those images, and then dynamically generating a download page where users can preview and download individual images or download all images in a zip file.

3. **Preview and Download**: On the download page, users can preview the images and choose to download individual images or click the "Download All Images" button to download all images as a zip file.

## Features

- **Image Preview**: Users can click on any image on the download page to view it in a larger modal window, enhancing the user experience by allowing for detailed image inspection before downloading.

- **Automatic Image Purging**: The application includes a background scheduler that periodically purges old images from the server, ensuring efficient use of server resources.

- **Responsive Design**: The application is designed with a responsive layout, ensuring a seamless user experience across various devices and screen sizes.

## Getting Started

To use the eBay Photo Downloader, simply navigate to the application's URL, enter the eBay listing URL into the designated field, and click the "Download Photos" button. The application will then guide you through the process of previewing and downloading the images.
