# Jhon.-j — Sales and Inventory Manager (Bookstore)
## Description
## Jhon.-j is a management system designed for bookstores. It allows you to:
Manage book inventory (add, update, delete, search, list).
Register sales and handle a shopping cart system.
Register clients and track their purchase history.
Generate reports such as top-selling books and sales grouped by author.
All code includes advanced validation and is thoroughly documented so any developer can understand and maintain it.
## Key Features
Full inventory CRUD (create, read, update, delete).
Sales system with cart functionality.
Automatic client registration with unique ID generation.
Complete client purchase histories.
Reports:
Individual client history (details, registration date, purchases, total spent).
Complete list of clients with their purchases.
Top 3 best-selling books (with all book details).
Sales grouped by author (total sales per author).
## System Structure and Menu Flow
# Main Menu
Options: Inventory, Sales, Reports, Exit.
# Inventory CRUD
Options (0–5):
0 — Return to main menu
1 — Add a book
2 — Update a book
3 — Delete a book
4 — Search for a book
5 — Show all books
All operations include input validation and user-friendly messages.
# Sales
Options:
1 — Add to cart / Register sale
Checks if the client is already registered.
If the client exists: the system adds the new purchase to their history (only if the sale is completed).
If the client does not exist: it registers them automatically and generates an ID.
If the purchase is completed, it is saved.
If not, only the client information is saved.
0 — Return to the main menu
# Reports (1–5; 5 = return)
1 — View a client’s purchase history (full details + total spent)
2 — View all clients and their purchases
3 — Top 3 best-selling books
4 — Sales grouped by author
5 — Return to main menu