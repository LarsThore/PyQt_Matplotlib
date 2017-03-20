#! encoding:utf8 #

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import time, glob, os

############################# Set Constants ###################################

H = 137100.               # Energy difference [J/mol]
R = 8.314               # Gas constant [J/(mol K)]

b = 250. * 10**(-9)    # nearest neighbour spacing [m]
T = (1050 + 273.15)     # Temperature [K]

############################## Functions ######################################

def remove_pictures():
    # Clean up old frames
    for name in glob.glob('tmp*.png'):
        os.remove(name)

def create_environment(n):
    # create environment in which there is a constant equilibrium
    # concentration at the left hand side boundary

    matrix = np.zeros((n, n))
    # matrix[:, 0] = np.round(np.random.ranf((5, n/2)) * 0.5284295)
    matrix[:, 0] = 1
    return matrix

def choose_atom(alu_ids):
    kk = np.random.randint(len(alu_ids))
    atom = alu_ids[kk]
    return atom

def move_atom(atom):

    i = atom[0]
    j = atom[1]

    global counter2
    counter2 += 1
    print "Atom no. {} moved".format(counter2)

    # move the atom back or forth

    # check if atom at the left border is chosen
    if j == 0:
        if matrix[i, j+1] == 0:
            matrix[i, j] = 1            # atom at left border is kept
            matrix[i, j+1] = 1
        else:
            pass
    # check if atom at the right border is chosen
    elif j == n-1:
        if matrix[i, j-1] == 0:
            matrix[i, j] = 0
            matrix[i, j-1] = 1
        else:
            pass
    # check if it collides with another Aluminum atom
    elif matrix[i, j+1] == 0 and matrix[i, j-1] == 0:
        matrix[i, j] = 0
        if np.random.randint(2) == 1:
            matrix[i, j+1] = 1
        else:
            matrix[i, j-1] = 1
    elif matrix[i, j+1] == 1 and matrix[i, j-1] == 0:
        if np.random.randint(2) == 1:
            matrix[i, j] = 0
            matrix[i, j-1] = 1
        else:
            pass
    elif matrix[i, j-1] == 1 and matrix[i, j+1] == 0:
        if np.random.randint(2) == 1:
            matrix[i, j] = 0
            matrix[i, j+1] = 1
        else:
            pass
    else:
        pass

    return matrix

def calc_time_increment(jump_art):
    # average time per jump
    N_diffusors = 1         # TODO find a reasonable value for number of diffusors

    tau = b**2 / (2 * D)
    random_R = np.log(np.random.uniform())
    tau_ = N_diffusors * tau            # after Lesar
    t_step = - tau_ * random_R
    return t_step

def make_plots(matrix, t, n, counter):

    # years = t_k // 31536000                             # number of years
    # weeks = (t_k % 31536000.) // (86400.*7)             # number of weeks
    # hours = (t_k % (86400*7)) // 3600.                   # number of hours
    # seconds = t_k % 3600.                               # number of seconds

    # create a figure
    fig1 = plt.figure(figsize=(12,1), facecolor='white')
    # add plot to the figure
    fig1.subplots_adjust(left=0.06, right=0.98, top=0.7, bottom=0.3, hspace=0.3, wspace=0.3)
    ax1 = fig1.add_subplot(211)
    im = ax1.imshow(matrix, aspect = 'auto')
    ax1.get_xaxis().set_ticks([])
    ax1.get_yaxis().set_ticks([])
    # plt.title("Temperature = {:.0f},\t $\Delta$t = {:.0f} years \t\t {:.0f} weeks \t\
    #  {:.0f} hours  \t\t{:.0f} sec".format(temp, years, weeks, hours, seconds))
    plt.title("Time = {:.1f} sec".format(t))

    plt.savefig('tmp_{:04d}.png'.format(counter))
    plt.clf()       # to delete the figure from the cache
    plt.close()     # to close the window

def make_plot2(average_over_position, positions):
    # create a figure
    plt.figure(facecolor='white')
    # add plot to the figure
    plt.plot(np.arange(n)*0.25 - (n*0.25 / 2), average_over_position)
    plt.title("Average Number of Atoms at particular Site")
    plt.xlabel('Distance from Interface [$\mu m$]')
    plt.ylabel('Aluminum Concentration')
    plt.xlim(- (n*0.25 / 2), (n*0.25 / 2))
    print 'Anzahl der Elemente in positions[:, 0]:', len(positions[:, 0])
    plt.savefig('Average_Concentration_{}.png'.format(
     len(positions[:, 0])))

def make_movie(n):
    from scitools.std import movie
    movie('tmp_*.png', encoder='convert', fps=4,
          output_file='tmp_diffusion_task3_system_size{}x{}.gif'.format(n, n))

############################### Precommands ###################################

remove_pictures()
time0 = time.time()

############################### main code #####################################

# set number of atoms in diffusion direction
n = 10                         # system size, length of one axis
t_end = 1000.                  # 1000 seconds annealing time

counter = 0                    # counter for pictures
counter2 = 0                   # counter for number of diffused atoms
counter2_list = []

round_list = [1]#2, 5002]#, 10000]

for rounds in round_list:
    positions_rounds = np.zeros((rounds, n))
    for j in range(rounds):
        t = 0.                  # initial time

        if j % 100 == 0:
            print j
            time.sleep(0.3)

        # positions_temp = np.zeros((temp_steps, n))
        matrix = create_environment(n)
        print matrix

        t_temp = 0.
        # set diffusion coefficient
        D = 1.49 * 10**(-7) * np.exp(-H/(R*T)) # in [m**2/s]

        # make fine time steps
        for m in range(2):         # TODO make a meaningful range

            # pick sites of Aluminum atoms
            for i in range(n):
                for j in range(n):

                    if matrix[i, j] == 1:
                        matrix = move_atom((i, j))

                        jump_art = 0      # kick_out_1, kick_out_2 or diffusion

                        print matrix

# --> hier weitermachen

                        # calculate the increment of time per jump
                        delta_t = calc_time_increment(jump_art)
                        t_temp += delta_t

                        make_plots(matrix, delta_t, n, counter)

        if t > t_end:
            break

        # if j % 100 == 0:
            # print "T: {} \t D: {:.2g} \t time: {:.2g} sec".format(
            #  temp, D, t)

        counter += 1

        # average_position_temp = np.average(positions_temp, axis = 0) #* temp_steps
        # positions_rounds[j] = average_position_temp

    # average_position_rounds = np.average(positions_rounds, axis = 0) #* temp_steps

    # make_plot2(average_position_rounds, positions_rounds)

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
