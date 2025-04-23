import pandas as pd
import operator


# operators dictionary
OPERATORS = {
    "==": { "func": operator.eq, "arity": 1 },
    "!=": { "func": operator.ne, "arity": 1 },
    ">": { "func": operator.gt, "arity": 1 },
    ">=": { "func": operator.ge, "arity": 1 },
    "<": { "func": operator.lt, "arity": 1 },
    "<=": { "func": operator.le, "arity": 1 },
    
    "isin": { 
        "func": lambda col, val: col.isin(val), 
        "arity": 1 
    },
    "contains": { 
        "func": lambda col, val: col.str.contains(val, na=False), 
        "arity": 1 
    },
    "startswith": { 
        "func": lambda col, val: col.str.startswith(val, na=False), 
        "arity": 1 
    },
    "endswith": { 
        "func": lambda col, val: col.str.endswith(val, na=False), 
        "arity": 1 
    },
    "empty": { 
        "func": lambda col, _: col.isnull() | (col == ""), 
        "arity": 0 
    },
    "between": { 
        "func": lambda col, val: col.between(val[0], val[1]), 
        "arity": 2 
    }
}

def filter_builder(node):
    """
    Builds a filter function for a pandas DataFrame from a dictionary structure.

     :param dict node: A dictionary representing the filter to be applied. 
        Keys for single nodes:
            - "key" (str): The column name in the DataFrame.
            - "operator" (str): The operator to use (e.g., ">", "==").
            - "value" (any): The value to compare against.
            - "valueIfNull" (optional, any): A fallback value to replace nulls 
              in the column (e.g., via fillna).
        Keys for connector nodes:
            - "connector" (str): The logical connector ("and", "or", "not").
            - "conditions" (list of dict, required for "and"/"or"): Sub-conditions.
            - "condition" (dict, required for "not"): Single sub-condition.

    :return A function to apply the filter to a pandas DataFrame.
    :rtype (pd.DataFrame) -> pd.Series[bool]
     
    """

    #single node
    if {"key", "operator"}.issubset(node):
        column = node["key"]
        op = node["operator"]
        
        if op not in OPERATORS:
            raise ValueError("Invalid operator")
        
        value = node.get("value", None)
        fallback = node.get("valueIfNull", None) 


        arity =  OPERATORS[op]["arity"]
        if arity != 0 and value is None:
                raise ValueError(f"The operator {op} takes {arity} arguments and does not accept None as value.")
        elif arity > 1:
            if isinstance(value, (list, dict, tuple)):
                #If value is a collection its length have to match the operator arity.
                length = len(value) 
                if length != arity:
                    raise ValueError(f"The operator {op} takes {arity} arguments, {length} given (key: {column}).")
            else:
                raise ValueError(f"The operator {op} takes a collection of {arity} arguments (key: {column}).")
  
               
        if fallback:
            return lambda df: OPERATORS[op]["func"](df[column].fillna(fallback), value)
        else:
            return lambda df: OPERATORS[op]["func"](df[column], value)
    
                                              

    #connector node
    if "connector" in node: 
        booleanConnector = node["connector"]
    
        if booleanConnector == "not":
            condition = filter_builder(node["condition"])
            return lambda data: ~ condition(data)
        else:
            conditions = [filter_builder(condition) for condition in node["conditions"]]
            if  booleanConnector == "and":
                return lambda df: pd.concat([condition(df) for condition in conditions], axis=1).all(axis=1)
            elif booleanConnector == "or":
                return lambda df: pd.concat([condition(df) for condition in conditions], axis=1).any(axis=1)           
            else:
                raise ValueError(f"Unsupported boolean operator :{booleanConnector}")

    raise ValueError("Syntax error.")
