import mysql.connector
from decimal import Decimal

# Connect to the MySQL Database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Replace with your MySQL host
        user="root",       # Replace with your MySQL username
        password="Priti@123#",       # Replace with your MySQL password
        database="picture_booking"
    )

def calculate_gst(ticket_price, no_of_tickets, gst_rate=18):
    total_price = Decimal(ticket_price) * no_of_tickets
    gst = (total_price * Decimal(gst_rate)) / Decimal(100)
    return total_price, gst

# Function to book a movie ticket
def book_ticket(customer_name, movie_id, no_of_tickets):
    db = connect_to_db()
    cursor = db.cursor()

    # Fetch movie details from the database
    cursor.execute("SELECT movie_name, ticket_price FROM movies WHERE movie_id = %s", (movie_id,))
    movie = cursor.fetchone()

    if movie:
        movie_name, ticket_price = movie
        total_price, gst = calculate_gst(ticket_price, no_of_tickets)
        
        # Insert the booking into the database
        cursor.execute("""
            INSERT INTO bookings (customer_name, movie_id, no_of_tickets, total_price, gst)
            VALUES (%s, %s, %s, %s, %s)
        """, (customer_name, movie_id, no_of_tickets, total_price, gst))

        # Commit the transaction and close the connection
        db.commit()
        print(f"Booking successful! Movie: {movie_name}, Total Price: {total_price + gst}, GST: {gst}")
    else:
        print("Movie not found.")
    
    db.close()

# Function to view available movies
def view_movies():
    db = connect_to_db()
    cursor = db.cursor()

    cursor.execute("SELECT movie_id, movie_name, ticket_price FROM movies")
    movies = cursor.fetchall()

    if movies:
        print("Available Movies:")
        for movie in movies:
            print(f"{movie[0]}. {movie[1]} - Ticket Price: {movie[2]}")
    else:
        print("No movies available.")
    
    db.close()

# Main function to interact with the user
def main():
    while True:
        print("\nMovie Ticket Booking System")
        print("1. View Movies")
        print("2. Book Ticket")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            view_movies()
        elif choice == '2':
            customer_name = input("Enter your name: ")
            movie_id = int(input("Enter movie ID: "))
            no_of_tickets = int(input("Enter number of tickets: "))
            book_ticket(customer_name, movie_id, no_of_tickets)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
