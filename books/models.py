from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=127)
    author = models.CharField(max_length=127)
    year = models.IntegerField()
    sinopsy = models.CharField(max_length=255, null=True)
    pages = models.IntegerField()

    users_following = models.ManyToManyField(
        "users.User", related_name="books_followed"
    )


# class Follow(models.Model):
#     book = models.ForeignKey(
#         "books.Book",
#         on_delete=models.CASCADE,
#         related_name="book_followers",
#     )

#     user = models.ForeignKey(
#         "users.User",
#         on_delete=models.CASCADE,
#         related_name="user_book_followers"
#     )
