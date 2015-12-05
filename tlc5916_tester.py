import tlc5916_driver

tlc5916_driver.set_pins(11,12,13,15);
#tlc5916_driver.set_debug(True);
tlc5916_driver.set_info(True);
tlc5916_driver.set_chips(4);
tlc5916_driver.set_offset(0);
tlc5916_driver.init();
tlc5916_driver.test();
#tlc5916_driver.clear_all_leds();
