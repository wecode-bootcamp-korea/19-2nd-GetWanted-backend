def user_infomation(user):

    results = {
        'title'    : f"{user.name}_{user.resume_set.count() + 1}",
        'fullName' : user.name,
        'email'    : user.email,
        'phone'    : user.phonenumber
    }
    return results