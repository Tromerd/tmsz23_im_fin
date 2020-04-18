import time


# time decorator
def get_time(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        response = func(*args, **kwargs)
        print(func.__name__, time.time() - start)
        return response

    return wrapper


# @get_time
def foo(*args, **kwargs):
    from django.http import JsonResponse
    time.sleep(1)
    json_data = {'current_time': time.time()}
    return JsonResponse({'response': json_data})


if __name__ == '__main__':
    pass
    # foo(3)
    # time.sleep(2)
    # foo(4)
    # time.sleep(2)
    # foo(5)
    # time.sleep(2)
    # foo(1)
    # foo()
