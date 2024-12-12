import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

class DatabaseModel:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='security_db',
                user='root',
                password=''
            )
            if self.connection.is_connected():
                print("Connected to MySQL database")
        except Error as e:
            print(f"Error: {e}")

    def verify_employee(self, employee_id):
        """Verify if an employee exists and get their details"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM employee WHERE id_employee = %s"
            print(f"Verifying employee with ID: {employee_id}")
            cursor.execute(query, (employee_id,))
            result = cursor.fetchone()
            print(f"Database result: {result}")
            cursor.close()
            return result
        except Error as e:
            print(f"Database error during verification: {e}")
            return None

    def get_employee_equipment(self, employee_id):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = """SELECT e.* FROM equipment e 
                      JOIN have h ON e.id_equipment = h.id_equipment 
                      WHERE h.id_employee = %s"""
            cursor.execute(query, (employee_id,))
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return []

    def assign_equipment(self, employee_id, equipment_id):
        """Assign equipment to employee and decrease quantity"""
        try:
            cursor = self.connection.cursor()
            
            # Vérifier la quantité disponible
            cursor.execute(
                "SELECT quantity_equipment FROM equipment WHERE id_equipment = %s",
                (equipment_id,)
            )
            result = cursor.fetchone()
            if not result or result[0] <= 0:
                print(f"Equipment {equipment_id} not available (quantity: {result[0] if result else 0})")
                return False
            
            # Diminuer la quantité
            cursor.execute(
                "UPDATE equipment SET quantity_equipment = quantity_equipment - 1 WHERE id_equipment = %s",
                (equipment_id,)
            )
            
            # Ajouter la relation
            cursor.execute(
                "INSERT INTO have (id_employee, id_equipment) VALUES (%s, %s)",
                (employee_id, equipment_id)
            )
            
            self.connection.commit()
            print(f"Equipment {equipment_id} assigned to employee {employee_id}")
            return True
            
        except Exception as e:
            print(f"Error assigning equipment: {e}")
            self.connection.rollback()
            return False

    def unassign_equipment(self, employee_id, equipment_id):
        """Unassign equipment from employee and increase quantity"""
        try:
            cursor = self.connection.cursor()
            
            # Supprimer la relation
            cursor.execute(
                "DELETE FROM have WHERE id_employee = %s AND id_equipment = %s",
                (employee_id, equipment_id)
            )
            
            # Augmenter la quantité
            cursor.execute(
                "UPDATE equipment SET quantity_equipment = quantity_equipment + 1 WHERE id_equipment = %s",
                (equipment_id,)
            )
            
            self.connection.commit()
            print(f"Equipment {equipment_id} unassigned from employee {employee_id}")
            return True
            
        except Exception as e:
            print(f"Error unassigning equipment: {e}")
            self.connection.rollback()
            return False

    def get_all_equipment(self):
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM equipment"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error: {e}")
            return []

    def get_all_employees(self):
        """Get all employees with their photos"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT * FROM employee"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error getting employees: {e}")
            return []

    def __del__(self):
        if hasattr(self, 'connection') and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")
