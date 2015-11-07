import tlc5916_driver
tlc5916_driver.init();
tlc5916_driver.set_debug(True);
tlc5916_driver.set_chips(2);
tlc5916_driver.set_offset(0);
tlc5916_driver.test();
tlc5916_driver.clear_all_leds();
