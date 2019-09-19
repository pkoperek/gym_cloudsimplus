class SwfJob(object):
    """Format as specified in
       http://www.cs.huji.ac.il/labs/parallel/workload/swf.html
    """

    def __init__(self,
                 job_id,
                 submit_time,
                 wait_time,
                 run_time,
                 allocated_cores,
                 mips_per_core):
        self._job_id = job_id
        self._submit_time = submit_time
        self._wait_time = wait_time
        self._run_time = run_time
        self._allocated_cores = allocated_cores
        self._mips_per_core = mips_per_core

    @property
    def mips_per_core(self):
        return self._mips_per_core

    @property
    def job_id(self):
        return self._job_id

    @property
    def submit_time(self):
        return self._submit_time

    @property
    def wait_time(self):
        return self._wait_time

    @property
    def run_time(self):
        return self._run_time

    @property
    def allocated_cores(self):
        return self._allocated_cores

    def as_cloudlet_descriptor_dict(self):
        return {
            'jobId': self.job_id,
            'submissionDelay': self.submit_time,
            'mi': self.run_time * self.mips_per_core * self.allocated_cores,
            'numberOfCores': self._allocated_cores,
        }


jobs = []

with open('LLNL-Atlas-2006-2.1-cln.swf', 'r') as f:
    for line in f.readlines():
        if line.startswith(';'):
            continue

        stripped = line.strip()
        splitted = stripped.split()

        job_id = splitted[0]
        submit_time = float(splitted[1])
        wait_time = float(splitted[2])
        run_time = splitted[3]
        allocated_cores = splitted[4]

        mips = 1250

        if int(run_time) > 0 and int(allocated_cores) > 0:
            job = SwfJob(
                job_id=int(job_id),
                submit_time=int(submit_time),
                wait_time=int(wait_time),
                run_time=int(run_time),
                allocated_cores=int(allocated_cores),
                mips_per_core=int(mips),
            )
            jobs.append(job.as_cloudlet_descriptor_dict())

