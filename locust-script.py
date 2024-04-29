from locust import FastHttpUser, task, constant_throughput
class TestUser(FastHttpUser):
    wait_time = constant_throughput({{ .Values.Rps }})
    
    @task
    def user_task(self):
        data = {
                "_id": "65485b4346e1a95572e5f40b",
                "index": 2,
                "guid": "3b8ef5b1-8f52-4284-9412-e185f2ac54a2",
                "isActive": False,
                "balance": "$1,934.07",
                "picture": "http://placehold.it/32x32",
                "age": 21,
                "eyeColor": "brown",
                "name": "Eleanor Bray",
                "gender": "female",
                "company": "ZAGGLES",
                "email": "eleanorbray@zaggles.com",
                "phone": "+1 (973) 519-3813",
                "address": "577 Cypress Court, Eggertsville, South Dakota, 7678",
                "about": "Enim dolore eiusmod duis veniam culpa commodo consectetur sunt eiusmod voluptate tempor excepteur Lorem. Dolor sit culpa ex eiusmod quis ad incididunt proident enim adipisicing esse culpa ea consequat. Cupidatat esse veniam aute labore eiusmod sit esse qui veniam duis. Adipisicing ipsum labore incididunt ad culpa velit amet ullamco proident in velit laborum. Id reprehenderit culpa in Lorem. Elit ipsum dolor irure occaecat amet. Et sit non aliquip in incididunt consequat in voluptate aliquip dolore.\r\n",
                "registered": "2014-07-14T01:12:11 -06:-30",
                "latitude": -60.722351,
                "longitude": 99.079594,
                "tags": [
                    "esse",
                    "qui",
                    "cupidatat",
                    "ullamco",
                    "dolore",
                    "nisi",
                    "anim"
                ],
                "friends": [
                    {
                        "id": 0,
                        "name": "Briana Brown"
                    },
                    {
                        "id": 1,
                        "name": "Angelica Compton"
                    },
                    {
                        "id": 2,
                        "name": "Miles House"
                    }
                ],
                "greeting": "Hello, Eleanor Bray! You have 3 unread messages.",
                "favoriteFruit": "strawberry"
            }
        self.client.request("POST", "/", json = data)