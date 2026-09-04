
from datetime import datetime, timedelta


class Travel:
    def __init__(self):
        """
        初始化系统，包含用户档案和航班信息
        """

        self.users = {
            "user1": {"user_name": "Eve", "password": "password123", "cash_balance": 2000.0, "bank_balance": 50000.0, "membership_level": "regular"},
            "user2": {"user_name": "Frank", "password": "password456", "cash_balance": 8000.0, "bank_balance": 8000.0, "membership_level": "silver"},
            "user3": {"user_name": "Grace", "password": "password789", "cash_balance": 1000.0, "bank_balance": 5000.0, "membership_level": "gold"}
        }


        self.flights = [
            {
                "flight_no": "CA1234",
                "origin": "北京",
                "destination": "上海",
                "depart_time": "2024-07-15 08:00:00",
                "arrival_time": "2024-07-15 10:30:00",
                "status": "available",
                "seats_available": 5,
                "economy_price": 1200,
                "business_price": 3000
            },
            {
                "flight_no": "MU5678",
                "origin": "上海",
                "destination": "北京",
                "depart_time": "2024-07-16 09:00:00",
                "arrival_time": "2024-07-16 11:30:00",
                "status": "available",
                "seats_available": 3,
                "economy_price": 1900,
                "business_price": 3000
            },
            {
                "flight_no": "CZ4321",
                "origin": "上海",
                "destination": "北京",
                "depart_time": "2024-07-16 20:00:00",
                "arrival_time": "2024-07-16 22:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 2500,
                "business_price": 4000
            },
            {
                "flight_no": "CZ4352",
                "origin": "上海",
                "destination": "北京",
                "depart_time": "2024-07-17 20:00:00",
                "arrival_time": "2024-07-17 22:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1600,
                "business_price": 2500
            },
            {
                "flight_no": "MU3561",
                "origin": "北京",
                "destination": "南京",
                "depart_time": "2024-07-18 08:00:00",
                "arrival_time": "2024-07-18 10:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 4000
            },
            {
                "flight_no": "MU1566",
                "origin": "北京",
                "destination": "南京",
                "depart_time": "2024-07-18 20:00:00",
                "arrival_time": "2024-07-18 22:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 4000
            },
            {
                "flight_no": "CZ1765",
                "origin": "南京",
                "destination": "深圳",
                "depart_time": "2024-07-17 20:30:00",
                "arrival_time": "2024-07-17 22:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 2500
            },
            {
                "flight_no": "CZ1765",
                "origin": "南京",
                "destination": "深圳",
                "depart_time": "2024-07-18 12:30:00",
                "arrival_time": "2024-07-18 15:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 2500
            },
            {
                "flight_no": "MH1765",
                "origin": "厦门",
                "destination": "成都",
                "depart_time": "2024-07-17 12:30:00",
                "arrival_time": "2024-07-17 15:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 2500
            },
            {
                "flight_no": "MH2616",
                "origin": "成都",
                "destination": "厦门",
                "depart_time": "2024-07-18 18:30:00",
                "arrival_time": "2024-07-18 21:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 2500
            },
            {
                "flight_no": "MH2616",
                "origin": "成都",
                "destination": "福州",
                "depart_time": "2024-07-16 18:30:00",
                "arrival_time": "2024-07-16 21:00:00",
                "status": "available",
                "seats_available": 8,
                "economy_price": 1500,
                "business_price": 2500
            }
        ]



        self.reservations = [
            {
                "reservation_id": "res_1",
                "user_id": "user1",
                "flight_no": "CA1234",
                "payment_method": "bank",
                "cabin": "经济舱",
                "baggage": 1,
                "origin": "北京",
                "destination": "上海",
            },
            {
                "reservation_id": "res_2",
                "user_id": "user1",
                "flight_no": "MU5678",
                "payment_method": "bank",
                "cabin": "商务舱",
                "baggage": 1,
                "origin": "上海",
                "destination": "北京",
            },
            {
                "reservation_id": "res_3",
                "user_id": "user2",
                "flight_no": "MH1765",
                "payment_method": "bank",
                "cabin": "商务舱",
                "baggage": 1,
                "origin": "厦门",
                "destination": "成都",
            },
            {
                "reservation_id": "res_4",
                "user_id": "user2",
                "flight_no": "MU2616",
                "payment_method": "bank",
                "cabin": "商务舱",
                "baggage": 1,
                "origin": "成都",
                "destination": "厦门",
            },
        ]


    def _load_scenario(self, scenario: dict, long_context=False) -> None:
        pass


    def get_flight_details(self, origin: str = None, destination: str = None) -> list:
        """
        根据出发地和到达地查询航班的基本信息。
        """
        flights = self.flights
        

        if origin:
            flights = [flight for flight in flights if flight["origin"] == origin]
        

        if destination:
            flights = [flight for flight in flights if flight["destination"] == destination]
        if len(flights) == 0:
            return f'没有符合条件的直达航班'

        return [{"flight_no": flight["flight_no"], "origin": flight["origin"], "destination": flight["destination"], 
                "depart_time": flight["depart_time"], "arrival_time": flight["arrival_time"], 
                "status": flight["status"], "seats_available": flight["seats_available"], 
                "economy_price": flight["economy_price"], "business_price": flight["business_price"]}
                for flight in flights]


    def get_user_details(self, user_id: str, password: str) -> dict:
        """
        根据用户名和密码查询用户信息
        """
        user = self.users.get(user_id)
        if user and user["password"] == password:
            return {key: value for key, value in user.items() if key != "password"}
        return {"status": "error", "message": "用户名或密码不正确"}
    

    def get_reservation_details(self, reservation_id: str = None, user_id: str = None) -> list:
        """
        根据预订ID或用户ID查询预订信息，包括对应航班的基本信息。
        """

        if reservation_id:
            reservations = [reservation for reservation in self.reservations if reservation["reservation_id"] == reservation_id]
        elif user_id:
            reservations = [reservation for reservation in self.reservations if reservation["user_id"] == user_id]
        else:
            return {"status": "error", "message": "请提供有效的预订ID或用户ID"}


        detailed_reservations = []
        for reservation in reservations:
            flight_info = next((flight for flight in self.flights if flight["flight_no"] == reservation["flight_no"]), None)
            detailed_reservation = {**reservation, "flight_info": flight_info}
            detailed_reservations.append(detailed_reservation)
        
        return detailed_reservations
    

    
    
    def authenticate_user(self, user_id, password):
        user = self.users.get(user_id)
        if user and user["password"] == password:
            return user
        return {"status": "error", "message": "用户名或密码不正确"}

    

    def get_baggage_allowance(self, membership_level, cabin_class):
        """
        获取用户基于会员等级和舱位的免费托运行李限额。

        参数:
        - membership_level (str): 会员等级 ("regular", "silver", "gold")
        - cabin_class (str): 舱位 ("基础经济舱", "经济舱", "商务舱")

        返回:
        - int: 免费托运行李数量
        """
        allowance = {
            "regular": { "经济舱": 1, "商务舱": 2},
            "silver": { "经济舱": 2, "商务舱": 3},
            "gold": {"经济舱": 3, "商务舱": 3}
        }
        return allowance.get(membership_level, {}).get(cabin_class, 0)
    

    def find_transfer_flights(self, origin_city, transfer_city, destination_city):
        """
        查找从出发城市到目的地城市的中转航班，确保第一班航班降落时间早于第二班航班起飞时间。
        :param origin_city: 出发城市
        :param transfer_city: 中转城市
        :param destination_city: 到达城市
        :return: 满足条件的中转航班列表，每个航班包含两段航程的信息。
        """

        first_leg_flights = [
            flight for flight in self.flights 
            if flight["origin"] == origin_city and flight["destination"] == transfer_city and flight["status"] == "available"
        ]


        second_leg_flights = [
            flight for flight in self.flights 
            if flight["origin"] == transfer_city and flight["destination"] == destination_city and flight["status"] == "available"
        ]


        transfer_flights = []


        for first_flight in first_leg_flights:
            first_arrival = datetime.strptime(first_flight["arrival_time"], "%Y-%m-%d %H:%M:%S")
            
            for second_flight in second_leg_flights:
                second_departure = datetime.strptime(second_flight["depart_time"], "%Y-%m-%d %H:%M:%S")
                

                if first_arrival < second_departure:
                    transfer_flights.append({
                        "first_leg": first_flight,
                        "second_leg": second_flight
                    })


        if transfer_flights:
            return transfer_flights
        else:
            return "未找到符合条件的中转航班。"
    

    def calculate_baggage_fee(self, membership_level, cabin_class, baggage_count):
        free_baggage = {"regular": {"经济舱": 1, "商务舱": 2}, "silver": {"经济舱": 2, "商务舱": 3}, "gold": {"经济舱": 3, "商务舱": 3}}
        free_limit = free_baggage[membership_level][cabin_class]
        additional_baggage = max(baggage_count - free_limit, 0)
        return additional_baggage * 50
    

    def update_balance(self, user, payment_method, amount):
        """
        更新用户的余额。
        :param user: 用户信息
        :param payment_method: 支付方式（"cash" 或 "bank"）
        :param amount: 更新金额（正数表示增加，负数表示减少）
        :return: 如果余额充足且更新成功，返回 True，否则返回 False。
        """
        if payment_method == "cash":
            if user["cash_balance"] + amount < 0:
                return False
            user["cash_balance"] += amount
        elif payment_method == "bank":
            if user["bank_balance"] + amount < 0:
                return False
            user["bank_balance"] += amount
        return True
    

    def reserve_flight(self, user_id, password, flight_no, cabin, payment_method, baggage_count):
        user = self.authenticate_user(user_id, password)
        if not user:
            return "认证失败，请检查用户ID和密码。"


        flight = next((f for f in self.flights if f["flight_no"] == flight_no and f["status"] == "available"), None)



        price = flight["economy_price"] if cabin == "经济舱" else flight["business_price"]
        total_cost = price


        baggage_fee = self.calculate_baggage_fee(user["membership_level"], cabin, baggage_count)
        total_cost += baggage_fee


        if payment_method not in ["cash", "bank"]:
                return "支付方式无效"
            

        if payment_method == "cash":
            if total_cost > self.users.get(user_id)["cash_balance"]:
                return f"cash余额不足，请考虑换一种支付方式"
            self.users.get(user_id)["cash_balance"] -= total_cost
        else:
            if total_cost > self.users.get(user_id)["bank_balance"]:
                return f"bank余额不足，请考虑换一种支付方式"
            self.users.get(user_id)["bank_balance"] -= total_cost


        flight["seats_available"] -= 1
        reservation_id = f"res_{len(self.reservations) + 1}"
        reservation = {
            "reservation_id": reservation_id,
            "user_id": user_id,
            "flight_no": flight_no,
            "payment_method": payment_method,
            "cabin": cabin,
            "baggage": baggage_count,
        }
        self.reservations.append(reservation)

        return f"预订成功，预订号：{reservation_id}，总费用：{total_cost}元（包含行李费用）。"


    def modify_flight(self, user_id, reservation_id, new_flight_no=None, new_cabin=None, add_baggage=0, new_payment_method=None):
        """
        修改航班预订，包括更改航班、舱位和行李。
        :param user_id: 用户ID
        :param reservation_id: 预订ID
        :param new_flight_no: 新的航班号（可选）
        :param new_cabin: 新的舱位（可选）
        :param add_baggage: 新增托运行李的数量（默认为0）
        :param new_payment_method: 新的付款方式（可选）
        """

        reservation = next((r for r in self.reservations if r['reservation_id'] == reservation_id and r['user_id'] == user_id), None)
        if not reservation:
            return "预订未找到或用户ID不匹配。"


        current_flight = next((f for f in self.flights if f['flight_no'] == reservation['flight_no']), None)
        if not current_flight:
            return "航班信息未找到。"


        payment_method = new_payment_method if new_payment_method else reservation['payment_method']
        user = self.users[user_id]
        if not user:
            return "用户信息未找到。"


        result_messages = []


        if new_flight_no and new_flight_no != reservation['flight_no']:

            new_flight = next((f for f in self.flights if f['flight_no'] == new_flight_no), None)
            if new_flight and new_flight['origin'] == current_flight['origin'] and new_flight['destination'] == current_flight['destination']:
                reservation['flight_no'] = new_flight_no
                result_messages.append("航班号已更改。")
            else:
                return f"航班更改失败：新的航班号无效或目的地不匹配。"


        if new_cabin and new_cabin != reservation.get('cabin'):
            price_difference = self.calculate_price_difference(current_flight, reservation['cabin'], new_cabin)
            reservation['cabin'] = new_cabin
            if price_difference > 0:

                if self.update_balance(user, payment_method, -price_difference):
                    result_messages.append(f"舱位更改成功。已支付差价: {price_difference}。")
                else:
                    result_messages.append("余额不足，无法支付舱位差价。")
            elif price_difference < 0:

                self.update_balance(user, payment_method, -price_difference)
                result_messages.append(f"舱位更改成功。已退款差价: {-price_difference}。")


        if add_baggage > 0:
            membership = user["membership_level"]
            max_free_baggage = self.get_baggage_allowance(membership, reservation['cabin'])
            current_baggage = reservation.get('baggage', 0)
            total_baggage = current_baggage + add_baggage
            extra_baggage = max(0, total_baggage - max_free_baggage)
            baggage_cost = extra_baggage * 50
            if baggage_cost > 0:

                if self.update_balance(user, payment_method, -baggage_cost):
                    result_messages.append(f"行李已增加。需支付额外费用: {baggage_cost}。")
                else:
                    result_messages.append("余额不足，无法支付额外行李费用。")
            reservation['baggage'] = total_baggage


        if not result_messages:
            result_messages.append("修改完成，无需额外费用。")
        return " ".join(result_messages)




    def cancel_reservation(self, user_id, reservation_id, reason):

        current_time = datetime(2024, 7, 14, 6, 0, 0)


        user = self.users.get(user_id, None)
        if not user:
            return "用户ID无效。"

        reservation = next((r for r in self.reservations if r["reservation_id"] == reservation_id and r["user_id"] == user_id), None)
        if not reservation:
            return "预订ID无效或与该用户无关。"


        flight = next((f for f in self.flights if f["flight_no"] == reservation["flight_no"]), None)
        if not flight:
            return "航班信息无效。"
        

        depart_time = datetime.strptime(flight["depart_time"], "%Y-%m-%d %H:%M:%S")
        if current_time > depart_time:
            return "航段已使用，无法取消。"


        time_until_departure = depart_time - current_time
        cancel_fee = 0
        refund_amount = 0


        flight_price = flight["economy_price"] if reservation["cabin"] == "经济舱" else flight["business_price"]


        if reason == "航空公司取消航班":

            refund_amount = flight_price
            self.process_refund(user, refund_amount)
            return f"航班已取消，您的预订将被免费取消，已退款{refund_amount}元。"

        elif time_until_departure > timedelta(days=1):

            refund_amount = flight_price
            self.process_refund(user, refund_amount)
            return f"距离出发时间超过24小时，免费取消成功，已退款{refund_amount}元。"
        
        else:

            cancel_fee = flight_price * 0.1
            refund_amount = flight_price - cancel_fee
            self.process_refund(user, refund_amount)
            return f"距离出发时间不足24小时，已扣除取消费{cancel_fee}元，退款{refund_amount}元。"

    def process_refund(self, user, amount):
        """
        将退款金额添加到用户的现金余额中。
        """
        user["cash_balance"] += amount
        print(f"已成功处理退款，{user['user_name']}的现金余额增加了{amount}元。")


    def calculate_price_difference(self, flight, old_cabin, new_cabin):
        """
        计算舱位价格差异。
        :param flight: 航班信息
        :param old_cabin: 原舱位等级
        :param new_cabin: 新舱位等级
        :return: 价格差异（正数表示需支付差价，负数表示退款）
        """
        cabin_prices = {
            "经济舱": flight["economy_price"],
            "商务舱": flight["business_price"]
        }
        old_price = cabin_prices.get(old_cabin, 0)
        new_price = cabin_prices.get(new_cabin, 0)
        return new_price - old_price


