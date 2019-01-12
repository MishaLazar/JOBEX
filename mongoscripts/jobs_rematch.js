var jobs = db.jobs.find({
        status: 0
    })
    .sort({ _id: -1 })
    .limit(100)