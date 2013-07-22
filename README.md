ordoro
======
A module for interacting with Magento product inventories via the SOAPv2 API.

Requires: eventlet, suds

Note: the test cases revealed several products whose inventory can't be updaetd via API call - it is always stuck at 0.  I believe this is because they are bundled or configurable products; solving this is beyond the scope of this project.
