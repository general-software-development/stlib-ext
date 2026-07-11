from src import vis, data

def main():
    values = [1, 2, 3, 4, 5]
    values.append(6)
    link = vis.VisLink(values)
    jsonv = vis.ViewJSON(values)
    print(link)
    print(jsonv)
    morevalues = {"test": 2, "test.more": "2.8"}
    print(vis.ViewJSON(morevalues))

    print(data.Number(8), data.Number("4"), data.Number("4.2"))

if __name__ == "__main__":
    main()

# This is a test file. This is not included in the library
