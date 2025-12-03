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

    max_score = 0

    for amounts in generate_combinations(len(ingredients), 100):
        score = calculate_score(ingredients, amounts)
        if score > max_score:
            max_score = score

    return max_score

def solve_part_2(input_data):
    ingredients = parse_ingredients(input_data)
    max_score = 0

    for amounts in generate_combinations(len(ingredients), 100):
        score, calories = calculate_score(ingredients, amounts, include_calories=True)
        if calories == 500 and score > max_score:
            max_score = score

    return max_score
