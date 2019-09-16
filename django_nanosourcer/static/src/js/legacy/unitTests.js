QUnit.test("Latitude", function(assert) {

    try {

        var latitude = new Latitude();
        assert.ok(false, "No exception thrown for an invalid parameter")

    } catch(error) {

        assert.ok(true, "Throws exception for invalid parameter")

    }

    try {

        var latitude = new Latitude(10.0);
        assert.ok(true, "Valid constructor parameter")

    } catch (error) {

        assert.ok(false, "Invalid constructor parameter")

    }

    try {

        var latitude = new Latitude(100.0);
        assert.ok(false, "Should throw exception because 100.0 is an invalid latitude value")

    } catch (error) {

        assert.ok(true, "Throws exception because 100.0 is an invalid latitude value")

    }

});
QUnit.test("Latitude", function(assert) {

    try {

        var longitude = new Longitude();
        assert.ok(false, "No exception thrown for an invalid parameter")

    } catch(error) {

        assert.ok(true, "Throws exception for invalid parameter")

    }

    try {

        var longitude = new Longitude(10.0);
        assert.ok(true, "Valid constructor parameter")

    } catch (error) {

        assert.ok(false, "Invalid constructor parameter")

    }

    try {

        var longitude = new Longitude(1000.0);
        assert.ok(false, "Should throw exception because 1000.0 is an invalid longitude value")

    } catch (error) {

        assert.ok(true, "Throws exception because 1000.0 is an invalid longitude value")

    }

});