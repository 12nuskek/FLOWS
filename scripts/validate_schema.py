import sqlite3
from pathlib import Path

def validate_schema():
    # Connect to the database
    db_path = Path('instance/flow.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name;
    """)
    tables = cursor.fetchall()
    
    print("Database Schema Validation:")
    print("==========================")
    
    for table in tables:
        table_name = table[0]
        print(f"\n{table_name}:")
        print("-" * (len(table_name) + 1))
        
        # Get column info for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Print column details
        for col in columns:
            cid, name, type_, notnull, dflt_value, pk = col
            constraints = []
            if pk:
                constraints.append("PRIMARY KEY")
            if notnull:
                constraints.append("NOT NULL")
            if dflt_value is not None:
                constraints.append(f"DEFAULT {dflt_value}")
                
            constraint_str = f" ({', '.join(constraints)})" if constraints else ""
            print(f"  - {name}: {type_}{constraint_str}")
            
        # Get foreign key info
        cursor.execute(f"PRAGMA foreign_key_list({table_name});")
        fks = cursor.fetchall()
        
        # Print foreign key details
        if fks:
            print("\n  Foreign Keys:")
            for fk in fks:
                _, _, ref_table, from_col, to_col, *_ = fk
                print(f"  - {from_col} -> {ref_table}({to_col})")
    
    conn.close()

if __name__ == '__main__':
    validate_schema() 