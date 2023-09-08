from redis.client import Redis

redis_password = "claTaHzjTMyLAKNkoRzX0RDw_cNHaKO1v6A2f4O1If07mu42SlY-KXIxftlj4jIVtWDYRbZX4WVmY4OHLBEzkm2XBoyZh_n2PkEFVJfYQO7Sf5dZGrp5Tp5eMKWDkfB5DnVvvtPQvRMsXDXkyIRw8u0sx7-LVhj3HORY0skH7axqxyRBoqG4_6Nh5bTRM9wMXNuwETUQxdpKiKorV5SSL9oWXcLxHDansp7ZZ4LxgOJ8uvSjWVrzDHjcXoUr72BL63wqTAL6PH4VB_qO-HvMKNl37ft0Fi6D0CI-XqtUxmuDk-W7gj_b8zJRy08I7lUeVgSi8I2ToE9RwMBbpdf-w"
timeout = 4000.0
redis_ip = "45.88.90.8"
global_redis_database_users = Redis(redis_ip, 6379, 0, redis_password, timeout)
global_redis_database_fc_3 = Redis(redis_ip, 6379, 8, redis_password, timeout)
global_redis_database_fc_4 = Redis(redis_ip, 6379, 8, redis_password, timeout)
global_redis_database_fc_101 = Redis(redis_ip, 6379, 8, redis_password, timeout)
global_redis_database_hc = Redis(redis_ip, 6379, 4, redis_password, timeout)
global_redis_database_rc = Redis(redis_ip, 6379, 5, redis_password, timeout)
global_redis_database_misc = Redis(redis_ip, 6379, 6, redis_password, timeout)
