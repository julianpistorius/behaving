import os
import time

from behave import step
from splinter.browser import Browser
from selenium.common.exceptions import WebDriverException


@step(u'a browser')
def given_a_browser(context):
    named_browser(context, '')


@step(u'browser "{name}"')
def named_browser(context, name):
    if name not in context.browsers:
        args = context.browser_args.copy()
        if context.remote_webdriver:
            args['driver_name'] = 'remote'
            if context.default_browser:
                args['browser'] = context.default_browser
        elif context.default_browser:
            args['driver_name'] = context.default_browser
        browser_attempts = 0
        while browser_attempts < context.max_browser_attempts:
            try:
                context.browsers[name] = Browser(**args)
                break
            except WebDriverException as e:
                browser_attempts += 1
        else:
            raise WebDriverException("Failed to initialize browser")
    context.browser = context.browsers[name]
    context.browser.switch_to_window(context.browser.windows[0])
    if context.default_browser_size:
        context.browser.driver.set_window_size(*context.default_browser_size)


@step(u'{brand} as the default browser')
def given_some_browser(context, brand):
    brand = brand.lower()
    context.default_browser = brand


@step(u'I reload')
def reload(context):
    context.browser.reload()


@step(u'I go back')
def go_back(context):
    context.browser.back()


@step(u'I go forward')
def go_forward(context):
    context.browser.forward()


@step(u'I resize the browser to {width}x{height}')
def resize_browser(context, width, height):
    context.browser.driver.set_window_size(int(width), int(height))


@step(u'I resize the viewport to {width}x{height}')
def resize_viewport(context, width, height):
    width = int(width)
    height = int(height)

    b_size = context.browser.driver.get_window_size()
    b_width = b_size['width']
    b_height = b_size['height']
    v_width = context.browser.evaluate_script("document.documentElement.clientWidth")
    v_height = context.browser.evaluate_script("document.documentElement.clientHeight")

    context.browser.driver.set_window_size(
        b_width + width - v_width,
        b_height + height - v_height)


@step(u'I take a screenshot')
def take_screenshot(context):
    assert context.browser is not None, u'need a browser to take a screenshot'
    assert context.screenshots_dir !='', u'no screenshots_dir specified'

    filename = context.scenario.feature.name + u'-' + \
        context.scenario.name + u'-' + \
        time.strftime("%Y-%m-%d-%H%M%S", time.gmtime(time.time()))
    filename = os.path.join(context.screenshots_dir, filename)
    context.browser.screenshot(filename)
