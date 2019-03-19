import unittest
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
import pdb

MyDir=os.path.dirname(__file__)
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from Polar import * 
from DynamicStall import * 

# Wagner - R.T Jones approximation (Jones 1938)
#Cl_wag_Jones=1-0.165*npexp(-0.0455*tau_t)-0.335*np.exp(-0.3*tau_t);
A1_Jones=0.165
A2_Jones=0.335
b1_Jones=0.0455
b2_Jones=0.3


def step_change():
    # --- 
    # We use a step from alpha0 to alpha0+2, testing mainly the circulatory response (history)
    # Oye's dynamic stall model will not give a proper response here:
    #  - We are in the linear region, f close to 1, resulting in mainly Cl_inv
    #  - There is no induction build-up (induction history) in the Oye's stall model itself
    #    Fs is continuous and progressive but not Cl since it uses the current alpha. 
    radians=True
    P=Polar.fromfile(os.path.join(MyDir,'../data/FFA-W3-241-Re12M.dat'),compute_params=True,to_radians=radians)
    if radians:
        deg_scale=np.pi/180
    else:
        deg_scale=1
    U0      = 10
    chord   = 0.1591
    alpha1  = P._alpha0 
    alpha2  = alpha1+2*deg_scale
    tau_oye = 3 * chord/U0
    tau_t   = np.linspace(0,30,1000)
    vt      = chord * tau_t / (2*U0)
       
    # Wagner function flatplate
    # Wagner - Garrick approximation (Garrick 1938)
    Cl_wag_Garr=(tau_t+2)/(tau_t+4);
    # Wagner - R.T Jones approximation (Jones 1938)
    #Cl_wag_Jones=1-0.165*npexp(-0.0455*tau_t)-0.335*np.exp(-0.3*tau_t);
    A1_Jones=0.165
    A2_Jones=0.335
    b1_Jones=0.0455
    b2_Jones=0.3
    # W.P. Jones (1945)
    #A1_Jones=0.165
    #A2_Jones=0.335
    #b1_Jones=0.041
    #b2_Jones=0.32

    Cl_wag_Jones=1-A1_Jones*np.exp(-b1_Jones*tau_t)-A2_Jones*np.exp(-b2_Jones*tau_t);
    # Flat plate params Jones


    # Oye's Parameters and Inputs
    p_oye=dict()
    u_oye=dict()
    u_oye['falpha']    = lambda t: alpha1 if t<= 0 else alpha2
    p_oye['tau']       = tau_oye
    p_oye['f_st_fun']  = P.f_st_interp
    p_oye['fClinv']    = P.cl_inv_interp
    p_oye['fClfs']     = P.cl_fs_interp

    # MHH Parameters and Inputs
    u=dict()
    p=dict()
    u['fU']         = lambda t: U0
    u['fU_dot']     = lambda t: 0 
    u['falpha']     = lambda t: alpha1 if t<=0 else alpha2 
    u['falpha_dot'] = lambda t: 0
    u['falpha_34']  = u['falpha']
    p['alpha0']    = P._alpha0
    p['Cla']       = P._linear_slope
    p['Tf']        = 3 * chord/U0
    p['Tp']        = 1.7 *chord/U0
    # NREL default
#     p['A1']        = 0.3
#     p['A2']        = 0.7
#     p['b1']        = 0.14
#     p['b2']        = 0.53
    # Flat Plate params
    p['A1']        = A1_Jones
    p['A2']        = A2_Jones
    p['b1']        = b1_Jones
    p['b2']        = b2_Jones
    # Riso A1-24 params
#     p['A1']        = 0.294
#     p['A2']        = 0.331
#     p['b1']        = 0.0664
#     p['b2']        = 0.3266
    p['chord']     = chord
    p['f_st_fun']  = P.f_st_interp
    p['cl_fs_fun'] = P.cl_fs_interp
    p['cd_fun']    = P.cd_interp

    # Steady values
    Cl_st1 = P.cl_interp(alpha1)
    Cl_st2 = P.cl_interp(alpha2)
    fs1    = P.f_st_interp(alpha1)        # init with steady value
    fs2    = P.f_st_interp(alpha2)        # init with steady value
    y0_mhh = dyna_stall_mhh_steady(0,u,p)
    y0_oye = [fs1]

    Cl_mhh  = np.zeros(len(vt))
    Cl_oye  = np.zeros(len(vt))
    # Integration using solve_ivp
    sol_mhh = solve_ivp(lambda t,x: dyna_stall_mhh_dxdt(t,x,u,p), t_span=[0, max(vt)], y0=y0_mhh, t_eval=vt)
    for it,t in enumerate(vt):
        Cl_mhh[it] = dyna_stall_mhh_outputs(t,sol_mhh.y[:,it],u,p)

    # Integration using solve_ivp
    sol_oye = solve_ivp(lambda t,x: dyna_stall_oye_dxdt(t,x,u_oye,p_oye), t_span=[0, max(vt)], y0=y0_oye, t_eval=vt)
    for it,t in enumerate(vt):
        Cl_oye[it] = dyna_stall_oye_output(vt[it],sol_oye.y[0,it],u_oye,p_oye)

    print('Cl steady:',Cl_st1,Cl_st2,Cl_mhh[0],Cl_oye[0])
    print('Fs steady:',fs1,fs2)

    fig=plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(tau_t,Cl_wag_Jones,'k'  ,label='Wagner - Jones')
    #ax.plot(tau_t,Cl_oye[:]/Cl_st2,'-' ,label = 'Cl dynamic (Oye)')
    ax.plot(tau_t[1:],Cl_mhh[1:]/Cl_st2 ,'--',label = 'Cl dynamic (MHH)')
    #ax.plot(tau_t,sol_oye.y[0,:]   ,'-' ,label = 'Fs (Oye)')
    #ax.plot(tau_t,sol_mhh.y[3,:] ,'--',label = 'Fs (MHH)')
    ax.set_xlabel('Dimensionless time [-]')
    ax.set_ylabel('Cl [-]')
    #ax.plot(tau_t,Cl_wag_Garr ,'k--',label='Wagner - Garr')
    plt.ylim([0.3,1.1])
    plt.legend()



# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def prescribed_oscillations_ris_r_1792():
    """
        See Riso-R-1792 report, p23-26 Figure 4.1 4.2
        """

    radians=True
    #FFA-W3-241 airfoil Dyna Stall
    P=Polar.fromfile(os.path.join(MyDir,'../data/DU21_A17.csv'),compute_params=True,to_radians=radians)

    if radians:
        deg_scale=np.pi/180
    else:
        deg_scale=1

    print('alpha0:',P._alpha0/deg_scale)

    K_omega    = 0.05    # reduced frequency k=omega*c/(2U0)
    U0         = 1
    chord      = 0.1591 # gives a omega of 12.57 with k=0.1, U0=10
    DeltaAlpha = 4.5
    # Parameters
    omega       = 2*U0*K_omega/chord
    T           = 2*np.pi/omega 
    tau_oye     = 4 * chord/U0
    valpha_mean = [0,10]
    valpha_mean = [-.5,9.5]
    t_max       = 1.3*T                  # simulation length
    dt          = 0.01                   # time step
    XLIM        = np.array([0,40])


    # Derived params
    vt       = np.arange(0,t_max,dt)
    Cl_mhh   = np.zeros((len(valpha_mean),len(vt)))
    Cl_oye   = np.zeros((len(valpha_mean),len(vt)))
    valpha_t = np.zeros((len(valpha_mean),len(vt)))

    # Loop on alpham and time 
    for ia,alpham in enumerate(valpha_mean):
        valpha_t[ia,:]   = (alpham+DeltaAlpha*np.sin(omega*vt))*deg_scale
        valpha_dot_t     = (2*omega*np.cos(omega*vt) )*deg_scale
        fs_prev = P.f_st_interp(alpham*deg_scale)# init with steady value

        # Oye's Parameters and Inputs
        p_oye=dict()
        u_oye=dict()
        u_oye['falpha']    = lambda t: np.interp(t, vt, valpha_t[ia,:])
        p_oye['tau']       = tau_oye
        p_oye['f_st_fun']  = P.f_st_interp
        p_oye['fClinv']    = P.cl_inv_interp
        p_oye['fClfs']     = P.cl_fs_interp

        # MHH Parameters and Inputs
        u=dict()
        p=dict()
        u['fU']         = lambda t: U0
        u['fU_dot']     = lambda t: 0
        u['falpha']     = lambda t: np.interp(t, vt, valpha_t[ia,:])
        u['falpha_dot'] = lambda t: np.interp(t, vt, valpha_dot_t)
        u['falpha_34']  = lambda t: np.interp(t, vt, valpha_t[ia,:]) # using alpha
        p['alpha0']     = P._alpha0
        p['Cla']        = P._linear_slope
        p['Tf']         = 3 * chord/U0
        p['Tp']         = 1.7 *chord/U0
        p['A1']         = A1_Jones
        p['A2']         = A2_Jones
        p['b1']         = b1_Jones
        p['b2']         = b2_Jones
        p['chord']      = chord
        p['f_st_fun']   = P.f_st_interp
        p['cl_fs_fun']  = P.cl_fs_interp
        p['cd_fun']     = P.cd_interp

        y0_mhh=[0,0,0,0]
        y0_oye=[0]
        y0_mhh = dyna_stall_mhh_steady(0,u,p)
        y0_oye = [fs_prev]



        # Oye - Integration using solve_ivp
        sol_oye = solve_ivp(lambda t,x: dyna_stall_oye_dxdt(t,x,u_oye,p_oye), t_span=[0, max(vt)], y0=y0_oye, t_eval=vt)
        for it,t in enumerate(vt):
            Cl_oye[ia,it] = dyna_stall_oye_output(vt[it],sol_oye.y[0,it],u_oye,p_oye)

        # Integration using solve_ivp
        sol_mhh = solve_ivp(lambda t,x: dyna_stall_mhh_dxdt(t,x,u,p), t_span=[0, t_max], y0=y0_mhh, t_eval=vt)
        for it,t in enumerate(vt):
            Cl_mhh[ia,it] = dyna_stall_mhh_outputs(t,sol_mhh.y[:,it],u,p)

    XLIM=[np.array([-5.10,4.10]),np.array([4.90,14.10])]
    YLIM=[np.array([-0.2,1.2]),np.array([1,1.7])]
    for ia,alpham in enumerate(valpha_mean):
        fig=plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(P.alpha/deg_scale  , P.cl  , label='Cl static', LineWidth=2)
        #ax.plot(valpha_t[ia,:]/deg_scale,Cl_oye[ia,:],'k--' ,label='Cl dynamic (Oye)')
        ax.plot(valpha_t[ia,:]/deg_scale,Cl_mhh[ia,:],'k-',label = 'Cl dynamic (MHH)')
        ax.set_xlabel('Alpha')
        ax.set_ylabel('Cl [-]')
        plt.xlim(XLIM[ia])
        plt.ylim(YLIM[ia])
        plt.legend()
        plt.grid()



# --------------------------------------------------------------------------------}
# ---  
# --------------------------------------------------------------------------------{
def prescribed_oscillations():
    radians=True
    #FFA-W3-241 airfoil Dyna Stall
    P=Polar.fromfile(os.path.join(MyDir,'../data/FFA-W3-241-Re12M.dat'),compute_params=True,to_radians=radians)

    if radians:
        deg_scale=np.pi/180
    else:
        deg_scale=1

    K_omega    = 0.1    # reduced frequency k=omega*c/(2U0)
    U0         = 10
    chord      = 0.1591 # gives a omega of 12.57 with k=0.1, U0=10
    DeltaAlpha = 4
    # Parameters
    omega       = 2*U0*K_omega/chord
    T           = 2*np.pi/omega 
    #omega=0
    #T           = 20
    tau         = 0.08
    tau_oye     = 4 * chord/U0
    valpha_mean = [5,10,15,20,25,30,35]
    #valpha_mean = [20]
    t_max       = 1.3*T                  # simulation length
    dt          = 0.01                   # time step
    XLIM        = np.array([0,40])


    # Derived params
    vt       = np.arange(0,t_max,dt)
    Cl_mhh   = np.zeros((len(valpha_mean),len(vt)))
    Cl_oye   = np.zeros((len(valpha_mean),len(vt)))
    valpha_t = np.zeros((len(valpha_mean),len(vt)))

    # Loop on alpham and time 
    for ia,alpham in enumerate(valpha_mean):
        valpha_t[ia,:]   = (alpham+DeltaAlpha*np.sin(omega*vt))*deg_scale
        valpha_dot_t     = (2*omega*np.cos(omega*vt) )*deg_scale
        fs_prev = P.f_st_interp(alpham*deg_scale)# init with steady value

        # Oye's Parameters and Inputs
        p_oye=dict()
        u_oye=dict()
        u_oye['falpha']    = lambda t: np.interp(t, vt, valpha_t[ia,:])
        p_oye['tau']       = tau_oye
        p_oye['f_st_fun']  = P.f_st_interp
        p_oye['fClinv']    = P.cl_inv_interp
        p_oye['fClfs']     = P.cl_fs_interp

        # MHH Parameters and Inputs
        u=dict()
        p=dict()
        u['fU']         = lambda t: U0
        u['fU_dot']     = lambda t: 0
        u['falpha']     = lambda t: np.interp(t, vt, valpha_t[ia,:])
        u['falpha_dot'] = lambda t: np.interp(t, vt, valpha_dot_t)
        u['falpha_34']  = lambda t: np.interp(t, vt, valpha_t[ia,:]) # using alpha
        p['alpha0']     = P._alpha0
        p['Cla']        = P._linear_slope
        p['Tf']         = 3 * chord/U0
        p['Tp']         = 1.7 *chord/U0
        p['b1']         = 0.14
        p['b2']         = 0.53
        p['A1']         = 0.3
        p['A2']         = 0.7
        p['chord']      = chord
        p['f_st_fun']   = P.f_st_interp
        p['cl_fs_fun']  = P.cl_fs_interp
        p['cd_fun']     = P.cd_interp

        y0_mhh=[0,0,0,0]
        y0_oye=[0]
        y0_mhh = dyna_stall_mhh_steady(0,u,p)
        y0_oye = [fs_prev]



        # Oye - Integration using solve_ivp
        sol_oye = solve_ivp(lambda t,x: dyna_stall_oye_dxdt(t,x,u_oye,p_oye), t_span=[0, max(vt)], y0=y0_oye, t_eval=vt)
        for it,t in enumerate(vt):
            Cl_oye[ia,it] = dyna_stall_oye_output(vt[it],sol_oye.y[0,it],u_oye,p_oye)

        # Integration using solve_ivp
        sol_mhh = solve_ivp(lambda t,x: dyna_stall_mhh_dxdt(t,x,u,p), t_span=[0, t_max], y0=y0_mhh, t_eval=vt)
        for it,t in enumerate(vt):
            Cl_mhh[ia,it] = dyna_stall_mhh_outputs(t,sol_mhh.y[:,it],u,p)

        #print('alpham    ', alpham*deg_scale, y0_mhh[0]+y0_mhh[1])
        #print('fst oye   ', y0_oye)
        #print('steady mhh', y0_mhh)
        #print('Cl mhh t0 ', dyna_stall_mh_outputs(t,y0_mhh,u,p))
        #print('Cl mhh t0 ', Cl_mh[ia,0])
        #print('Cl oye t0 ', Cl_oye[ia,0])
        #print('Cl oye t0 ', P.cl_interp(alpham*deg_scale))


        #fig=plt.figure()
        #ax = fig.add_subplot(111)
#       #  ax.plot(vt,sol_mh.y[0,:],label='x1')
        #ax.plot(vt,sol_mh.y[0,:]+sol_mh.y[1,:],label='alphaE')
        ##  alphaF  = x3/Cla+alpha0                                  # p. 13
        #ax.plot(vt,sol_mh.y[2,:]/P._linear_slope+P._alpha0,label='alphaF')
        #ax.plot(vt,valpha_t[ia,:],label='alpha')
        #ax.plot(vt,sol_mh.y[3,:],label='x4')
        #ax.plot(vt,sol.y[0,:]  ,label='f_st')
        ##ax.plot(vt,Cl_mh[ia,:],label='Cl_mh')
        ##ax.plot(vt,Cl_oye[ia,:],label='Cl_oy')
        #fig.legend()
        #print(sol_mh.y[:,-1])
        #print(dyna_stall_mh_steady(0,u,p))
        #print(Cl_mh[ia,-1])
        #print(P.cl_interp(alpham*deg_scale))



    for ia,alpham in enumerate(valpha_mean):
        fig=plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(P.alpha/deg_scale  , P.cl  , label='Cl static', LineWidth=2)
        if ia==0:
            lbl1='Cl dynamic (Oye)'
            lbl2='Cl dynamic (MHH)'
        else:
            lbl1=''
            lbl2=''
        ax.plot(valpha_t[ia,:]/deg_scale, Cl_oye[ia,:], 'k-'   , label=lbl1)
        ax.plot(valpha_t[ia,:]/deg_scale, Cl_mhh[ia,:] , 'k--'   , label=lbl2)
        ax.set_xlabel('Alpha')
        ax.set_ylabel('Cl [-]')
        plt.xlim(XLIM[ia])
#     plt.ylim([0,2.2])
        plt.legend()

if __name__ == '__main__':
    prescribed_oscillations_ris_r_1792()
    #prescribed_oscillations()
    #step_change()

    plt.show()
