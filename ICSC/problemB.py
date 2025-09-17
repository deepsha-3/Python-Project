import sys

def cake_calculator(flour: int, sugar: int) -> list:
   """
   Calculates the maximum number of cakes that can be made and the leftover ingredients.
   
   Args:
       flour: An integer larger than 0 specifying the amount of available flour.
       sugar: An integer larger than 0 specifying the amount of available sugar.
       
   Returns:
       A list of three integers: 
       [0] the number of cakes that can be made
       [1] the amount of leftover flour
       [2] the amount of leftover sugar
       
   Raises:
       ValueError: If inputs flour or sugar are not positive.
   """
   # Step 1: Validate inputs
   if flour <= 0 or sugar <= 0:
       raise ValueError("Flour and sugar must be positive integers.")

   # Step 2: Define the recipe requirements
   flour_per_cake = 100  # units
   sugar_per_cake = 50   # units

   # Step 3: Calculate how many cakes each ingredient allows
   maximum_cakes_by_flour = flour // flour_per_cake
   maximum_cakes_by_sugar = sugar // sugar_per_cake

   # Step 4: The actual number of cakes is limited by the scarcest ingredient
   cakes_made = min(maximum_cakes_by_flour, maximum_cakes_by_sugar)

   # Step 5: Calculate leftovers
   flour_left = flour - (cakes_made * flour_per_cake)
   sugar_left = sugar - (cakes_made * sugar_per_cake)

   # Step 6: Return results as a list
   return [cakes_made, flour_left, sugar_left]


# --- Main execution block. DO NOT MODIFY  ---
if __name__ == "__main__":
   try:
       # 1. Read input from stdin
       flour_str = input().strip()
       sugar_str = input().strip()
       
       # 2. Convert inputs to appropriate types
       flour = int(flour_str)
       sugar = int(sugar_str)
       
       # 3. Call the cake calculator function
       result = cake_calculator(flour, sugar)
       
       # 4. Print the result to stdout in the required format
       print(f"{result[0]} {result[1]} {result[2]}")
       
   except ValueError as e:
       # Handle errors during input conversion or validation
       print(f"Input Error or Validation Failed: {e}", file=sys.stderr)
       sys.exit(1)
   except EOFError:
       # Handle cases where not enough input lines were provided
       print("Error: Not enough input lines provided.", file=sys.stderr)
       sys.exit(1)
   except Exception as e:
       # Catch any other unexpected errors
       print(f"An unexpected error occurred: {e}", file=sys.stderr)
       sys.exit(1)
