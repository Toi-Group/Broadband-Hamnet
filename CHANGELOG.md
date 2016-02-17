## 0.4 (20160217)

Features:
- ToiChatMessage Protocol. Implemented using Google's Protobuf serializing
method (issue #1 #3)
- Built in DNS handling (issue #5)
- New ToiChat CLI (issue #4)
- Using the new CLI there is a better display out for one to one messaging
(issue #12)

Performance:
- DNS will connect to the closest ToiChat neighbor upon forcedns function
call (issue #8)