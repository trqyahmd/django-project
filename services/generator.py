import string
import random

chars = string.digits + string.ascii_letters

class CodeGenerator:
    @staticmethod
    def code_slug_generator(size, chars=chars):
        return "".join(random.choice(chars) for _ in range(size))

    @classmethod
    def create_slug_shortcode(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(code=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def create_slug_shortcode_profile(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(slug=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code

    @classmethod
    def create_activation_link_code(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(activation_link=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code
    
    @classmethod
    def create_product_code(cls, size, model_):
        new_code = cls.code_slug_generator(size=size)
        qs_exists = model_.objects.filter(activation_link=new_code).exists()
        return cls.create_slug_shortcode(size, model_) if qs_exists else new_code
    

# chars_productcode = "kumo" + string.digits + string.ascii_letters

# class ProductCodeGenerator:
#     @staticmethod
#     def code_slug_pc_generator(size, chars=chars_productcode):
#         return "".join(random.choice(chars) for _ in range(size))
    
#     @classmethod
#     def create_product_code(cls, size, model_):
#         new_product_code = cls.code_slug_pc_generator(size=size)
#         qs_exists = model_.objects.filter(code=new_product_code).exists()
#         return cls.create_slug_shortcode(size, model_) if qs_exists else new_product_code

class ProductCodeGenerator:
    @staticmethod
    def code_slug_pc_generator(size, chars=string.digits + string.ascii_letters):
        return "#KUMO" + "".join(random.choice(chars) for _ in range(size-len("kumo")))
    
    @classmethod
    def create_product_code(cls, size, model_):
        new_product_code = cls.code_slug_pc_generator(size=size)
        qs_exists = model_.objects.filter(code=new_product_code).exists()
        return cls.create_product_code(size, model_) if qs_exists else new_product_code