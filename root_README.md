# WolfWR Retail Management System

The WolfWR Retail Management System is a comprehensive application for managing retail operations including store administration, staff and supplier management, customer transactions, reporting, and more. The system is built using Python and MariaDB, with modular design separating database connectivity, command-line interaction, and a user-friendly text-based menu interface.

---

## cli.py

This CLI file serves as the main command-line interface for the WolfWR Retail Management System, coordinating operations across various functional modules such as store, staff, supplier, merchandise, transactions, and reports. It employs Python's argparse module to define subcommands and options for each operation, and uses a dictionary to dynamically map the provided command (group and action) to the corresponding handler function. Additionally, it enforces role-based access control by checking user permissions against each command group, ensuring that users can only perform allowed operations. This centralized CLI framework streamlines the execution of complex CRUD operations and reporting tasks by integrating all the system's modules into one cohesive entry point.

---

## db.py

This **db.py** file manages database connectivity for the WolfWR Retail Management System. It includes functions to read database configuration details from a configuration file using the ConfigParser module and to establish a connection to a MariaDB database with appropriate error handling via try/except blocks. The `connect_to_db` function creates and returns a connection object with autocommit disabled, ensuring that database transactions are explicitly controlled, while a helper function, `close_connection`, is available to properly close the connection when operations are complete. This centralized approach simplifies access to the database across the application, ensures robust error management, and prevents resource leaks by enforcing proper connection cleanup.

---

## menu.py

This code file implements a user-friendly, text-based interactive menu for the WolfWR Retail Management System. It displays a main menu with options including Store, Staff, Supplier, Club Member, Merchandise, Customer Transaction, Supplier Transaction, Discount, Signup, Reports, and Return Item, and for each selection, it directs the user to the corresponding submenu. In each submenu, the program prompts the user to provide necessary input details (e.g., IDs, dates, names, quantities, etc.) and then calls the appropriate functions from various handler and report modules to perform CRUD operations or generate reports. The design continuously loops to allow multiple operations until the user decides to exit, ensuring that all system functionalities are easily accessible and managed interactively.

---

## config.ini

This **config.ini** file provides the database connection parameters for the WolfWR Retail Management System. The file contains a single section named `[database]` with keys specifying the host, port, user credentials, and database name. These details are read by the `read_db_config` function in **db.py** to establish a connection with the MariaDB server.
