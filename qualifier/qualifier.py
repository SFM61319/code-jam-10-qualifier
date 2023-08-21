from PIL import Image


def is_unique(collection: list[int]) -> bool:
    """
    Return True if the given list is unique and all elements are in the range [0, len(collection)),
    False otherwise.
    """

    collection = sorted(collection)
    return all(i == el for i, el in enumerate(collection))


def get_tile(
    image: Image.Image, tile_size: tuple[int, int], i: int, j: int
) -> Image.Image:
    """
    Return the tile of size `tile_size` at the position (`i`, `j`) in the `image`.
    """

    tile_width, tile_height = tile_size
    x, y = tile_width * i, tile_height * j

    return image.crop((x, y, x + tile_width, y + tile_height))


def valid_input(
    image_size: tuple[int, int], tile_size: tuple[int, int], ordering: list[int]
) -> bool:
    """
    Return True if the given input allows the rearrangement of the image, False otherwise.

    The tile size must divide each image dimension without remainders, and `ordering` must use each
    input tile exactly once.
    """

    image_width, image_height = image_size
    tile_width, tile_height = tile_size
    tile_rows = image_height // tile_height
    tile_cols = image_width // tile_width

    return (
        image_width % tile_width == 0
        and image_height % tile_height == 0
        and len(ordering) == tile_rows * tile_cols
        and is_unique(ordering)
    )


def rearrange_tiles(
    image_path: str, tile_size: tuple[int, int], ordering: list[int], out_path: str
) -> None:
    """
    Rearrange the image.

    The image is given in `image_path`. Split it into tiles of size `tile_size`, and rearrange them
    by `ordering`.
    The new image needs to be saved under `out_path`.

    The tile size must divide each image dimension without remainders, and `ordering` must use each
    input tile exactly once. If these conditions do not hold, raise a ValueError with the message:
    "The tile size or ordering are not valid for the given image".
    """

    with (
        Image.open(image_path) as image,
        Image.new(image.mode, image.size) as out_image,
    ):
        image_size = image.size
        image_width, image_height = image_size
        tile_width, tile_height = tile_size
        tile_rows = image_height // tile_height
        tile_cols = image_width // tile_width

        if not valid_input(image_size, tile_size, ordering):
            raise ValueError(
                "The tile size or ordering are not valid for the given image"
            )

        tiles: list[Image.Image] = []
        out_tiles: list[Image.Image] = []

        for i in range(tile_rows):
            for j in range(tile_cols):
                tile = get_tile(image, tile_size, j, i)
                tiles.append(tile)

        for i in range(len(tiles)):
            out_tiles.append(tiles[ordering[i]])

        for i in range(tile_rows):
            for j in range(tile_cols):
                out_image.paste(
                    out_tiles[i * tile_cols + j], (tile_width * j, tile_height * i)
                )

        out_image.save(out_path)
