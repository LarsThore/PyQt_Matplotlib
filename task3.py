#! encoding:utf8 #

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time, glob, os

############################# Set Constants ###################################

H = 137100.               # Energy difference [J/mol]
R = 8.314               # Gas constant [J/(mol K)]

b = 2.34 * 10**(-10)    # distance between atom side and tetrahedral site [m]
d = 2.7 * 10**(-10)    # distance between two tetrahedral sites [m]

############## set equilibrium concentration at left hand side ################

equil_conc = 5.38e-2

############################## Functions ######################################

def remove_pictures():
    # Clean up old frames
    for name in glob.glob('tmp*.png'):
        os.remove(name)

def create_environment(n):
    # create environment in which there is a constant equilibrium
    # concentration at the left hand side boundary
    # matrix = np.zeros((n, n))
    # print matrix[:, 0]
    # print  np.round(np.random.ranf((1, n/2)) * 0.5284295)
    # matrix[:, 0] = np.round(np.random.ranf((1, n/2)) * 0.5284295)

    matrix = np.zeros((n))
    matrix[:n/2] = np.round(np.random.ranf((1, n/2)) * 5./9)
    matrix = matrix.reshape((1, n))
    return matrix

    # TODO soft code the calculation for the huge float number two lines above
    # which is dependent on equil_conc

    return matrix

def choose_atom(alu_ids):
    kk = np.random.randint(len(alu_ids))
    atom = alu_ids[kk]
    return atom

def move_atom(atom):
    global counter2
    counter2 += 1
    print "Atom no. {} moved".format(counter2)
    # move the atom back or forth
    # check if atom at the left border is chosen
    if atom == 0:
        if matrix[0][atom+1] == 0:
            matrix[0][atom] = 0
            matrix[0][atom+1] = 1
        else:
            pass
    # check if atom at the right border is chosen
    elif atom == n-1:
        if matrix[0][atom-1] == 0:
            matrix[0][atom] = 0
            matrix[0][atom-1] = 1
        else:
            pass
    # check if it collides with another Aluminum atom
    elif matrix[0][atom+1] == 0 and matrix[0][atom-1] == 0:
        matrix[0][atom] = 0
        if np.random.randint(2) == 1:
            matrix[0][atom+1] = 1
        else:
            matrix[0][atom-1] = 1
    elif matrix[0][atom+1] == 1 and matrix[0][atom-1] == 0:
        matrix[0][atom] = 0
        matrix[0][atom-1] = 1
    elif matrix[0][atom-1] == 1 and matrix[0][atom+1] == 0:
        matrix[0][atom] = 0
        matrix[0][atom+1] = 1
    else:
        pass

    return matrix

def calc_time_increment(alu_ids):
    # average time per jump
    tau = b**2 / (2 * D)
    random_R = np.log(np.random.uniform())
    B = len(alu_ids) * tau                        # after Lesar
    t_step = - B * random_R
    return t_step

def make_plots(matrix, vis_matrix, temp, t, n, counter):

    # years = t_k // 31536000                             # number of years
    # weeks = (t_k % 31536000.) // (86400.*7)             # number of weeks
    # hours = (t_k % (86400*7)) // 3600.                   # number of hours
    # seconds = t_k % 3600.                               # number of seconds

    # create a figure
    fig1 = plt.figure(figsize=(12,1), facecolor='white')
    # add plot to the figure
    fig1.subplots_adjust(left=0.06, right=0.98, top=0.7, bottom=0.3, hspace=0.3, wspace=0.3)
    ax1 = fig1.add_subplot(211)
    im = ax1.imshow(vis_matrix, aspect = 'auto')
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    # plt.title("Temperature = {:.0f},\t $\Delta$t = {:.0f} years \t\t {:.0f} weeks \t\
    #  {:.0f} hours  \t\t{:.0f} sec".format(temp, years, weeks, hours, seconds))
    plt.title("Temperature = {:.0f}, \t\t{:.1f} sec".format(
     temp, t))

    x = np.arange(n)
    y = np.zeros(n)
    p = n/10
    q = n/10
    ratios = np.zeros(n)
    for k in range(p, len(matrix[0][p:-p]) + p):
        counter1 = 0.
        for j in matrix[0][k-q:k+q]:
            if abs(j - 1) < 1e-6:
                counter1+= 1
        ratios[k] = counter1 / p

    ax2 = fig1.add_subplot(212)
    im2 = ax2.plot(ratios)
    ax2.set_xlim([0, n])
    ax2.set_ylim([0, 0.35])
    ax2.get_xaxis().set_ticks([])
    ax2.get_yaxis().set_ticks([])
    plt.savefig('tmp_{:04d}.png'.format(counter))
    plt.clf()       # to delete the figure from the cache
    plt.close()     # to close the window

def make_plot2(average_over_position, positions):
    # create a figure
    plt.figure(facecolor='white')
    # add plot to the figure
    plt.plot(average_over_position)
    plt.title("Average Number of Atoms at particular Site")
    plt.xlabel('Site Number')
    plt.ylabel('Occupation Ratio')
    print 'Anzahl der Elemente in positions[:, 0]:', len(positions[:, 0])
    plt.savefig('Average_Concentration_{}.png'.format(
     len(positions[:, 0])))

def make_movie():
    from scitools.std import movie
    movie('tmp_*.png', encoder='convert', fps=4,
          output_file='tmp_diffusion_task1.gif')

############################### Precommands ###################################

remove_pictures()
time0 = time.time()

############################### main code #####################################

# set number of atoms in diffusion direction
n = 50

t_end = 1000.

temp_steps = 101             # number of steps in temperature intervall
temperature = np.zeros((temp_steps))
temperature += (1050 + 273.15)

counter = 0
counter2 = 0
counter2_list = []

round_list = [1]#, 4000, 10000]

# calculate the time intervall
t_k = t_end / temp_steps

for rounds in round_list:
    positions_rounds = np.zeros((rounds, n, n))
    for j in range(rounds):
        t = 0.                  # initial time
        if j % 2 == 0:
            print j
            time.sleep(0.3)
        positions_temp = np.zeros((temp_steps, n, n))
        matrix = create_environment(n)

        for k, temp in enumerate(temperature):
            t_temp = 0.
            # set diffusion coefficient
            D = 1.49 * 10**(-7) * np.exp(-H/(R*temp)) # in [m**2/s]

            # positions is the array of the model copied many
            # times on below another
            positions_temp[k] = matrix

            # pick indices of Aluminum sites
            alu_atom = np.where(matrix == 1)
            alu_ids = alu_atom[1]
            if len(alu_ids) == 0:
                break

            counter3 = 0

            # make fine time steps
            # while t_temp < t_k:
            for m in range(10000):  # TODO make a meaningful range
                atom = choose_atom(alu_ids)
                matrix = move_atom(atom)

                # calculate the increment of time per jump
                delta_t = calc_time_increment(alu_ids)
                t_temp += delta_t

                counter3 += 1

            # make big time steps
            else:
                if counter3 == 1:
                    t += t_k
                else:
                    t += t_temp

            if t > t_end:
                break

            # if j % 100 == 0:
                # print "T: {} \t D: {:.2g} \t time: {:.2g} sec".format(
                #  temp, D, t)

            counter += 1

        average_position_temp = np.average(positions_temp, axis = 0) #* temp_steps
        positions_rounds[j] = average_position_temp

    average_position_rounds = np.average(positions_rounds, axis = 0) #* temp_steps

    make_plot2(average_position_rounds, positions_rounds)

    counter2_list.append(counter2)
    counter2 = 0

    ############################### End Commanfs #################################

    # print out time, make movie, remove picture files, print time to convert
    # pictures into gif file


    time1 = time.time()

    print 'Simulation time: {} minutes and {:2d} seconds'.format(
     int((time1 - time0) // 60), int((time1 - time0) % 60))

    # if rounds == round_list[-1]:
    #     make_movie()

    remove_pictures()

    print 'Conversion time to GIF: {} minutes and {:2d} seconds'.format(
     int((time.time() - time1) // 60), int((time.time() - time1) % 60))


print 'Atoms moved:', counter2_list
