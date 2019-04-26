db.users.aggregate([
    {
     "$addFields": { 
        "s_id": { 
            "$toString": "$_id" 
        }
        
          
        
    }
    },
     {
     $lookup:{
             from: "student_skills",
             localField:"s_id",
             foreignField: "student_id",
             as: "student_skills"
         }
         
     },
     {
         $match:{
             $and:[{s_id:"5cbdbe62f4578f2eb8853f44"}]
         }
     }
    //  ,{ $unwind:"$student_skills"},
    //   {
    //       $project:{
    //           _id:0,
    //           "student_skills.student_skill_list":1
    //       }
    //   }
     ])