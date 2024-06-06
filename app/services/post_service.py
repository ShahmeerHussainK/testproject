from typing import List

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.models import Post, User
from app.schemas import PostCreate
from cachetools import TTLCache

cache = TTLCache(maxsize=100, ttl=300)

class PostService:
    @staticmethod
    def add_post(db: Session, post: PostCreate, user: User) -> Post:
        """
        Adds a new post to the database.

        Args:
            db (Session): The database session object.
            post (PostCreate): The post data to be added.
            user (User): The user who is creating the post.

        Returns:
            Post: The newly created post object.

        Raises:
            ValueError: If the user is not valid.
            SQLAlchemyError: If there is an issue with the database transaction.
        """
        if not user:
            raise ValueError("Invalid user")

        try:
            db_post = Post(text=post.text, owner_id=user.id)
            db.add(db_post)
            db.commit()
            db.refresh(db_post)
            return db_post
        except SQLAlchemyError as e:
            db.rollback()
            # Log the error message if logging is set up in your application
            print(f"Database error occurred: {e}")
            raise
        except Exception as e:
            db.rollback()
            # Log the error message if logging is set up in your application
            print(f"An unexpected error occurred: {e}")
            raise

    @staticmethod
    # Assuming 'cache' is a dictionary defined somewhere in your code
    def get_posts(db: Session, user: User) -> List[Post]:
        """
        Retrieves posts for a given user, using a cache to optimize performance.

        Args:
            db (Session): The database session object.
            user (User): The user whose posts are being retrieved.

        Returns:
            List[Post]: A list of posts for the user.

        Raises:
            ValueError: If the user is not valid.
            SQLAlchemyError: If there is an issue with the database query.
        """
        if not user:
            raise ValueError("Invalid user")

        try:
            if user.id in cache:
                return cache[user.id]

            posts = db.query(Post).all()

            cache[user.id] = posts
            return posts

        except SQLAlchemyError as e:
            # Log the error message if logging is set up in your application
            print(f"Database error occurred: {e}")
            raise
        except Exception as e:
            # Log the error message if logging is set up in your application
            print(f"An unexpected error occurred: {e}")
            raise

    @staticmethod
    def delete_post(db: Session, post_id: int, user: User) -> Post:
        """
        Deletes a post for a given user.

        Args:
            db (Session): The database session object.
            post_id (int): The ID of the post to be deleted.
            user (User): The user attempting to delete the post.

        Returns:
            Post: The deleted post object.

        Raises:
            HTTPException: If the post is not found or the user is not valid.
            SQLAlchemyError: If there is an issue with the database transaction.
            ValueError: If the user is not valid.
        """
        if not user:
            raise ValueError("Invalid user")

        try:
            post = db.query(Post).filter(Post.id == post_id, Post.owner_id == user.id).first()
            if not post:
                raise HTTPException(status_code=404, detail="Post not found")

            db.delete(post)
            db.commit()
            return post

        except SQLAlchemyError as e:
            db.rollback()
            # Log the error message if logging is set up in your application
            print(f"Database error occurred: {e}")
            raise
        except HTTPException as e:
            # Rethrow HTTP exceptions without logging/rollback as they indicate client errors
            raise
        except Exception as e:
            db.rollback()
            # Log the error message if logging is set up in your application
            print(f"An unexpected error occurred: {e}")
            raise
