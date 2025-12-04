import re

def parse_ingredients(input_data):
    ingredients = []
    for line in input_data.strip().split('\n'):
        match = re.match(r'(\w+): capacity (-?\d+), durability (-?\d+), flavor (-?\d+), texture (-?\d+), calories (-?\d+)', line)
        if match:
            name = match.group(1)
            capacity = int(match.group(2))
            durability = int(match.group(3))
            flavor = int(match.group(4))
            texture = int(match.group(5))
            calories = int(match.group(6))
            ingredients.append({
                'name': name,
                'capacity': capacity,
                'durability': durability,
                'flavor': flavor,
                'texture': texture,
                'calories': calories
            })
    return ingredients

def calculate_score(ingredients, amounts, include_calories=False):
    total_capacity = sum(ingredients[i]['capacity'] * amounts[i] for i in range(len(ingredients)))
    total_durability = sum(ingredients[i]['durability'] * amounts[i] for i in range(len(ingredients)))
    total_flavor = sum(ingredients[i]['flavor'] * amounts[i] for i in range(len(ingredients)))
    total_texture = sum(ingredients[i]['texture'] * amounts[i] for i in range(len(ingredients)))

    # Negative totals become 0
    total_capacity = max(0, total_capacity)
    total_durability = max(0, total_durability)
    total_flavor = max(0, total_flavor)
    total_texture = max(0, total_texture)

    score = total_capacity * total_durability * total_flavor * total_texture

    if include_calories:
        total_calories = sum(ingredients[i]['calories'] * amounts[i] for i in range(len(ingredients)))
        return score, total_calories

    return score

def generate_combinations(num_ingredients, total_teaspoons):
    if num_ingredients == 1:
        yield [total_teaspoons]
        return

    for amount in range(total_teaspoons + 1):
        for rest in generate_combinations(num_ingredients - 1, total_teaspoons - amount):
            yield [amount] + rest

def solve_part_1(input_data):
    ingredients = parse_ingredients(input_data)
    n = len(ingredients)

    # Pre-compute property arrays for faster access
    capacity = [ing['capacity'] for ing in ingredients]
    durability = [ing['durability'] for ing in ingredients]
    flavor = [ing['flavor'] for ing in ingredients]
    texture = [ing['texture'] for ing in ingredients]

    max_score = 0

    for amounts in generate_combinations(n, 100):
        # Inline score calculation for speed
        c = max(0, sum(capacity[i] * amounts[i] for i in range(n)))
        d = max(0, sum(durability[i] * amounts[i] for i in range(n)))
        f = max(0, sum(flavor[i] * amounts[i] for i in range(n)))
        t = max(0, sum(texture[i] * amounts[i] for i in range(n)))
        score = c * d * f * t

        if score > max_score:
            max_score = score

    return max_score

def solve_part_2(input_data):
    ingredients = parse_ingredients(input_data)
    n = len(ingredients)

    # Pre-compute property arrays for faster access
    capacity = [ing['capacity'] for ing in ingredients]
    durability = [ing['durability'] for ing in ingredients]
    flavor = [ing['flavor'] for ing in ingredients]
    texture = [ing['texture'] for ing in ingredients]
    calories_arr = [ing['calories'] for ing in ingredients]

    max_score = 0

    for amounts in generate_combinations(n, 100):
        # Check calories first (early exit)
        cal = sum(calories_arr[i] * amounts[i] for i in range(n))
        if cal != 500:
            continue

        # Inline score calculation for speed
        c = max(0, sum(capacity[i] * amounts[i] for i in range(n)))
        d = max(0, sum(durability[i] * amounts[i] for i in range(n)))
        f = max(0, sum(flavor[i] * amounts[i] for i in range(n)))
        t = max(0, sum(texture[i] * amounts[i] for i in range(n)))
        score = c * d * f * t

        if score > max_score:
            max_score = score

    return max_score
