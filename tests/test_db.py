from backend.utils.utils import get_connection, get_nearest_eva, get_eva_by_name
from datetime import datetime


# TODO: current limitation only direct connections
def main():
    dt = datetime(2026, 5, 23, 10, 0)
    aug_hbf = get_eva_by_name("Augsburg Hbf")
    print(aug_hbf)
    conn = get_connection(aug_hbf["eva"], "München Hbf", dt)
    print(conn)


if __name__ == "__main__":
    main()
