import streamlit as st
import requests

# Function to search books using the Google Books API
def search_books(query, api_key=None):
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query}

    if api_key:  # Use the API key if provided
        params['key'] = api_key

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data from Google Books API")
        return None

# Streamlit app layout
def main():
    st.title("Google Books Search App")
    st.write("Search for books by title using the Google Books API")

    # Input field for the book title
    query = st.text_input("Enter book title")

    # Retrieve API key from Streamlit secrets
    api_key = st.secrets["GOOGLE_BOOKS_API_KEY"]

    if query:
        # Call the search_books function with the query and API key
        results = search_books(query, api_key)

        if results and 'items' in results:
            for item in results['items']:
                volume_info = item.get('volumeInfo', {})
                st.write(f"### {volume_info.get('title', 'No Title')}")
                authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
                st.write(f"**Author(s):** {authors}")
                st.write(f"**Published Date:** {volume_info.get('publishedDate', 'N/A')}")

                # Display book cover if available
                if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks']:
                    st.image(volume_info['imageLinks']['thumbnail'], width=150)

                # Display book description if available
                description = volume_info.get('description', 'No description available.')
                st.write(f"**Description:** {description}")

                st.write("---")
        else:
            st.write("No books found. Please try another title.")

if __name__ == "__main__":
    main()
