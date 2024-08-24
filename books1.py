import streamlit as st
import requests

# Function to search books using the Open Library API
def search_books(title):
    url = "https://openlibrary.org/search.json"
    params = {'title': title}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error fetching data from Open Library API")
        return None

# Streamlit app layout
def main():
    st.title("Book Search App")
    st.write("Search for books by title using the Open Library API")

    # Input field for the book title
    title = st.text_input("Enter book title")

    if title:
        results = search_books(title)
        
        if results and results.get('docs'):
            for book in results['docs'][:2]:  # Displaying top 10 results
                st.write(f"### {book.get('title')}")
                authors = ', '.join(book.get('author_name', ['Unknown Author']))
                st.write(f"**Author(s):** {authors}")
                st.write(f"**First Publish Year:** {book.get('first_publish_year', 'N/A')}")
                
                # Display book cover if available
                cover_id = book.get('cover_i')
                if cover_id:
                    cover_url = f"http://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    st.image(cover_url, width=150)
                
                # Display book plot/description if available
                description = book.get('first_sentence') or book.get('subtitle') or "No description available."
                st.write(f"**Description:** {description}")
                
                st.write("---")
        else:
            st.write("No books found. Please try another title.")

if __name__ == "__main__":
    main()
