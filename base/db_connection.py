import sqlite3
from utils import DB_PATH, DB_FILE

class DbConnection:
    
    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH + DB_FILE)
        self.cursor = self.connection.cursor()

    def get_materials(self):
        return self.cursor.execute('SELECT * FROM material').fetchall()

    def get_colours(self):
        return self.cursor.execute('SELECT * FROM colour').fetchall()

    def get_densities(self):
        return self.cursor.execute('SELECT * FROM density').fetchall()

    def get_diameters(self):
        return self.cursor.execute('SELECT * FROM diameter').fetchall()

    def save_materials(self, materials):
        for mat in materials:
            self.cursor.execute('INSERT INTO material(name) VALUES(?)', (mat,))
        self.connection.commit()

    def save_colours(self, colours):
        for mat in colours:
            self.cursor.execute('INSERT INTO colour(name) VALUES(?)', (mat,))
        self.connection.commit()

    def save_densities(self, densities):
        for mat in densities:
            self.cursor.execute('INSERT INTO density(value) VALUES(?)', (mat,))
        self.connection.commit()

    def save_diameters(self, diameters):
        for mat in diameters:
            self.cursor.execute('INSERT INTO diameter(value) VALUES(?)', (mat,))
        self.connection.commit()

    def get_custom_program_by_id(self, id):
        return self.cursor.execute('SELECT * FROM program where id = ?', (id,)).fetchall()[0]

    def get_all_custom_program(self):
        return self.cursor.execute('SELECT * FROM program').fetchall()

    def edit_custom_program(self, id, name, pressure, duration, temperature, preheating, subcicles):
        self.cursor.execute('UPDATE program SET name = ?, pressure = ?, duration = ?, temperature = ?, pre_heating_time = ?, subcicles =? where id = ?',
                 (name, pressure, duration, temperature, preheating, subcicles, id))

    def delete_custom_program(self, id):
        self.cursor.execute('DELETE FROM program WHERE id = ?', (id,))

    def save_custom_program(self, name, pressure, duration, temperature, preheating, subcicles):
        self.cursor.execute('INSERT INTO program(name, pressure, duration, temperature, pre_heating_time, subcicles) VALUES(?,?,?,?,?,?)',
                 (name, pressure, duration, temperature, preheating, subcicles))
        self.connection.commit()