import threading
import time
from p4p.nt import NTScalar
from p4p.server import Server
from p4p.server.thread import SharedPV

write_pv = SharedPV(nt=NTScalar('d'), initial=0.0)
readback_pv = SharedPV(nt=NTScalar('d'), initial=0.0)
stop_pv = SharedPV(nt=NTScalar('b'), initial=False)
dmov_pv = SharedPV(nt=NTScalar('b'), initial=True)
movn_pv = SharedPV(nt=NTScalar('b'), initial=False)
miss_pv = SharedPV(nt=NTScalar('b'), initial=False)
homf_pv = SharedPV(nt=NTScalar('b'), initial=False)
homr_pv = SharedPV(nt=NTScalar('b'), initial=False)
velo_pv = SharedPV(nt=NTScalar('d'), initial=5.0)
off_pv = SharedPV(nt=NTScalar('d'), initial=0.0)
hlm_pv = SharedPV(nt=NTScalar('d'), initial=100.0)
llm_pv = SharedPV(nt=NTScalar('d'), initial=0.0)
lvio_pv = SharedPV(nt=NTScalar('b'), initial=False)
lls_pv = SharedPV(nt=NTScalar('b'), initial=False)
hls_pv = SharedPV(nt=NTScalar('b'), initial=False)
cnen_pv = SharedPV(nt=NTScalar('b'), initial=True)
egu_pv = SharedPV(nt=NTScalar('s'), initial="mm")
sevr_pv = SharedPV(nt=NTScalar('d'), initial=0)
stat_pv = SharedPV(nt=NTScalar('d'), initial=0)
rdbd_pv = SharedPV(nt=NTScalar('d'), initial=0.01)
desc_pv = SharedPV(nt=NTScalar('s'), initial="a fake motor")
foff_pv = SharedPV(nt=NTScalar('b'), initial=False)
set_pv = SharedPV(nt=NTScalar('b'), initial=False)


def move():
    while True:
        time_stamp = time.time()
        curr_pos = readback_pv.current().raw.value
        new_pos = write_pv.current().raw.value
        if curr_pos < new_pos and abs(new_pos - curr_pos) > 0.1:
            curr_pos += 0.1
            readback_pv.post(curr_pos, timestamp=time_stamp)
            if dmov_pv.current().raw.value:
                dmov_pv.post(False, timestamp=time_stamp)
                movn_pv.post(True, timestamp=time_stamp)
        elif curr_pos > new_pos and abs(new_pos - curr_pos) > 0.1:
            curr_pos -= 0.1
            readback_pv.post(curr_pos, timestamp=time_stamp)
            if dmov_pv.current().raw.value:
                dmov_pv.post(False, timestamp=time_stamp)
                movn_pv.post(True, timestamp=time_stamp)
        elif curr_pos == new_pos:
            if not dmov_pv.current().raw.value:
                dmov_pv.post(True, timestamp=time_stamp)
                movn_pv.post(False, timestamp=time_stamp)
        else:
            readback_pv.post(new_pos, timestamp=time_stamp)
        time.sleep(0.1)


rb_thread = threading.Thread(target=move, daemon=True)
rb_thread.start()


@write_pv.put
def change_setpoint(pv, op):
    pv.post(op.value(), timestamp=time.time())
    op.done()


@stop_pv.put
def do_stop(pv, op):
    curr_pos = readback_pv.current().raw.value
    write_pv.post(curr_pos, timestamp=time.time())
    op.done()


Server.forever(providers=[{
    'fake:motor': write_pv,
    'fake:motor.VAL': write_pv,
    'fake:motor.RBV': readback_pv,
    'fake:motor.STOP': stop_pv,
    'fake:motor.DMOV': dmov_pv,
    'fake:motor.MOVN': movn_pv,
    'fake:motor.MISS': miss_pv,
    'fake:motor.HOMF': homf_pv,
    'fake:motor.HOMR': homr_pv,
    'fake:motor.VELO': velo_pv,
    'fake:motor.OFF': off_pv,
    'fake:motor.LLM': llm_pv,
    'fake:motor.HLM': hlm_pv,
    'fake:motor.LVIO': lvio_pv,
    'fake:motor.LLS': lls_pv,
    'fake:motor.HLS': hls_pv,
    'fake:motor.CNEN': cnen_pv,
    'fake:motor.EGU': egu_pv,
    'fake:motor.SEVR': sevr_pv,
    'fake:motor.STAT': stat_pv,
    'fake:motor.RDBD': rdbd_pv,
    'fake:motor.DESC': desc_pv,
    'fake:motor.FOFF': foff_pv,
    'fake:motor.SET': set_pv,
}])
