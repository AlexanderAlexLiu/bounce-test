def segment_intersection(segment1, segment2):
    xdiff = (segment1[0][0] - segment1[1][0], segment2[0][0] - segment2[1][0])
    ydiff = (segment1[0][1] - segment1[1][1], segment2[0][1] - segment2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
        return None

    d = (det(*segment1), det(*segment2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    if (segment1[0][0] <= x <= segment1[1][0] or segment1[1][0] <= x <= segment1[0][0]) and \
        (segment1[0][1] <= y <= segment1[1][1] or segment1[1][1] <= y <= segment1[0][1]) and \
        (segment2[0][0] <= x <= segment2[1][0] or segment2[1][0] <= x <= segment2[0][0]) and \
            (segment2[0][1] <= y <= segment2[1][1] or segment2[1][1] <= y <= segment2[0][1]):
        return x, y
    return None

print(segment_intersection(((0, 0), (100, 0)), ((50, 100), (50, -100))))