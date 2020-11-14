course_enrollments = [
            {
                '$lookup': {
                    'from': 'enrollment',
                    'localField': 'user_id',
                    'foreignField': 'user_id',
                    'as': 'enrollments'
                }
            }, {
                '$unwind': {
                    'path': '$enrollments',
                    'includeArrayIndex': 'enrollments_id',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$lookup': {
                    'from': 'course',
                    'localField': 'enrollments.course_id',
                    'foreignField': 'course_id',
                    'as': 'courses'
                }
            }, {
                '$unwind': {
                    'path': '$courses',
                    'preserveNullAndEmptyArrays': False
                }
            }, {
                '$match': {
                    'user_id': 1
                }
            }, {
                '$sort': {
                    'course_id': 1
                }
            }
        ]