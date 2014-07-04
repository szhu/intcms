#!/usr/bin/env python


def main():
    from intcms import parse_environment
    parse_environment()
    from intcms import Environment, PAGE, TEMPLATES, get_http_info
    env = Environment.create_jinja_env(PAGE, TEMPLATES, get_http_info())

    import extensions

    response = env.get_page(PAGE)
    response.print_header()
    response.print_content()

if __name__ == '__main__':
    main()
