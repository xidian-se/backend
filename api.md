# API 文档

## POST

### /register/tenant

租客注册，请求体结构

```json
{
  "name": "",
  "address": "",
  "sex": "",
  "phone": "",
  "birth": "",
  "username": "",
  "password": ""
}
```

返回结构
```json
{
  "isSuccess": true, // 失败的话是 false
  "reason": "信息"
}
```

### /register/owner

业主注册，请求体结构

```json
{
  "name": "",
  "address": "",
  "phone": "",
  "username": "",
  "password": ""
}
```

返回结构

```json
{
  "isSuccess": true, // 失败的话是 false
  "reason": "信息"
}
```

### /tenant/update

租客信息更新，请求体结构

```json
{
  "name": "",
  "address": "",
  "sex": "",
  "phone": "",
  "birth": "",
  "username": "",
  "password": ""
}
```

返回结构

### /owner/update

业主信息更新，请求体结构

```json
{
  "name": "",
  "address": "",
  "phone": "",
  "username": "",
  "password": ""
}
```

返回结构

### /login

用户登录，请求体结构

```json
{
  "username": "",
  "password": ""
}
```

返回结构
```json
{
  "isLogin": true,
  "identity": true,
  "data": {//看是啥类型用户返回的啥},
  "reason": "如果 isLogin 是 false 错误信息",
}
```

### /owner/houseinfo

1.参数 op 为 1，添加房屋信息，请求体结构

```json
{
  "name": "",
  "address": "",
  "total": 0,
  "rent": 0,
  "price": 0,
  "description": ""
}
```

返回结构

2.参数 op 为 2，更新房屋信息，请求体结构

```json
{
  "id": "",
  "name": "",
  "address": "",
  "total": 0,
  "rent": 0,
  "price": 0,
  "description": ""
}
```

返回结构

### /owner/cancel

请求结构

```json
{
  "id": "" // 租房操作id（其实就是租房对应关系的id）
}
```

返回结构

看着办，别忘了加上

下面是 copilot 自动生成的

```json
{
  "code": 0,
  "msg": "success"
}
```

### /owner/confirm

请求结构

```json
{
  "id": "" ,// 租房操作id（其实就是租房对应关系的id）
  "state": true/false // 确认租房或者取消租房
}
```

返回结构

看着办，别忘了加上

## GET

### /owner/houseinfo

1.参数为 id，需要返回某个房屋信息

返回结构

```json
{
  "name": "",
  "address": "",
  "total": 0,
  "rent": 0,
  "price": 0,
  "description": ""
}
```

2.无参数，需要返回此业主的所有房屋信息

返回结构

```json
[
  {
    "id": "",
    "name": "",
    "address": "",
    "total": 0,
    "rent": 0,
    "price": 0,
    "description": ""
  },
  {
    "id": "",
    "name": "",
    "address": "",
    "total": 0,
    "rent": 0,
    "price": 0,
    "description": ""
  }
]
```

### /owner/opinfo

无参数

返回结构

json 数组的第一个是未确定的租房信息，需要房主改变状态，第二个是正在租的信息，可以进行退租操作,也是一个数组，外层为房屋，children 内为租客，每个房屋为外层数组的一个元素。例如下

```json
[
  {
    "id": "", // 租房操作id（其实就是租房对应关系的id）
    "name": "", // 房屋名称
    "tenant": "", // 租客姓名
    "phone": "" // 租客电话
  },
  [
    {
      "name": "", // 租房操作id（其实就是租房对应关系的id）
      "children": [
        {
          "id": "", // 租房操作id（其实就是租房对应关系的id）
          "tenant": "", // 租客姓名
          "phone": "" // 租客电话
        },
        {
          "id": "", // 租房操作id（其实就是租房对应关系的id）
          "tenant": "", // 租客姓名
          "phone": "" // 租客电话
        }
      ]
    },
    {
      "name": "", // 租房操作id（其实就是租房对应关系的id）
      "children": [
        {
          "id": "", // 租房操作id（其实就是租房对应关系的id）
          "tenant": "", // 租客姓名
          "phone": "" // 租客电话
        },
        {
          "id": "", // 租房操作id（其实就是租房对应关系的id）
          "tenant": "", // 租客姓名
          "phone": "" // 租客电话
        }
      ]
    }
  ]
]
```
