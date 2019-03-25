# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *
if parse_args().virtual_keyboard:
    from src.core.api.keyboard.Xkeyboard import type
else:
    from src.core.api.keyboard.keyboard_api import type


class Test(FirefoxTest):

    @pytest.mark.DETAILS(
        description="Created to test fake keyboard inputs",
        locale='[en-US]',
    )
    def test_run(self):
        history_empty_pattern = Pattern('history_empty.png')
        if OSHelper.is_mac():
            clear_recent_history_last_hour_pattern = Pattern('sanitize_duration_choice_last_hour')

        # Open some pages to create some history.
        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected_1, 'Mozilla page loaded successfully.')

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert_true(self, expected_2, 'Firefox page loaded successfully.')

        # Open the History sidebar.
        history_sidebar()

        # Open the Clear Recent History window and select 'Everything'.
        for step in open_clear_recent_history_window():
            assert_true(self, step.resolution, step.message)
        if OSHelper.is_mac():
            click(clear_recent_history_last_hour_pattern)
            for i in range(4):
                type(Key.DOWN)
            type(Key.ENTER)

        else:
            for i in range(4):
                type(Key.DOWN)

        logger.debug('TAB')
        type(Key.TAB)
        logger.debug('TAB')
        type(Key.TAB)
        for i in range(5):
            type(Key.DOWN)
        logger.debug('SPACE')
        type(Key.SPACE)
        type(Key.DOWN)
        type(Key.SPACE)
        logger.debug('ENTER')
        type(Key.ENTER)

        # Sometimes Firefox is in a state where it can't receive keyboard input
        # and we need to restore the focus manually.
        restore_firefox_focus()

        # Check that all the history was cleared.
        expected_4 = exists(history_empty_pattern.similar(0.9), 10)
        assert_true(self, expected_4, 'All the history was cleared successfully.')
