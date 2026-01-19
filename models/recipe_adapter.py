class RecipeAdapter:
    @staticmethod
    def parse(recipe):
        # Jika sudah dict, kembalikan (dengan konversi nilai ke int).
        if isinstance(recipe, dict):
            return {k: int(v) for k, v in recipe.items()}
       
        # Jika format lain (misal list string "item:qty"), adaptasikan.
        parsed = {}
        try:
            for entry in recipe:
                if isinstance(entry, str) and ':' in entry:
                    key, val = entry.split(':', 1)
                    parsed[key.strip()] = int(val.strip())
        except TypeError:
            return {}
        return parsed