import streamlit as st
import requests

def search_books(query, api_key=None):
    """Searches for books using the Google Books API.

    Args:
        query: The search query.
        api_key: The Google Books API key (optional).

    Returns:
        A dictionary containing the search results, or None if an error occurred.
    """

    url = "https://www.googleapis.com/books/v1/volumes"
    params = {'q': query}

    if api_key:
        params['key'] = api_key

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from Google Books API: {e}")
        return None

def main():
    st.title("Google Books Search App")
    st.write("Search for books by title using the Google Books API")

    # Input field for the book title
    query = st.text_input("Enter book title")

    # Retrieve API key securely from Streamlit secrets
    api_key = st.secrets["GOOGLE_BOOKS_API_KEY"]

    if query:
        # Call the search_books function with the query and API key
        results = search_books(query, api_key)

        if results and 'items' in results:
            for item in results['items']:
                volume_info = item.get('volumeInfo', {})

                # Display book title or a default message
                st.write(f"### {volume_info.get('title', 'No Title Found')}")

                # Handle missing or multiple authors
                authors = ', '.join(volume_info.get('authors', ['Unknown Author']))
                st.write(f"**Author(s):** {authors}")

                # Display published date or a default message
                published_date = volume_info.get('publishedDate', 'N/A')
                st.write(f"**Published Date:** {published_date}")

                # Display book cover if available
                if 'imageLinks' in volume_info and 'thumbnail' in volume_info['imageLinks']:
                    st.image(volume_info['imageLinks']['thumbnail'], width=150)

                # Display book description or a default message
                description = volume_info.get('description', 'No description available.')
                st.write(f"**Description:** {description}")

                # Add a horizontal separator between books
                st.write("---")
        else:
            st.write("No books found. Please try another title.")

if __name__ == "__main__":
    main()
