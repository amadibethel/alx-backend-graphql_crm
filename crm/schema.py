import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")

class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        pass  # No input arguments needed for this mutation

    success = graphene.String()
    updated_products = graphene.List(ProductType)

    def mutate(root, info):
        # Find products with stock < 10
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_products = []

        for product in low_stock_products:
            product.stock += 10  # Simulate restock
            product.save()
            updated_products.append(product)

        return UpdateLowStockProducts(
            success=f"{len(updated_products)} product(s) restocked successfully.",
            updated_products=updated_products,
        )

class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()

schema = graphene.Schema(mutation=Mutation)

